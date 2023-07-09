from rest_framework import viewsets
from rest_framework.generics import mixins
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from django.views import View
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
import json,io
from django.db.models import Q 
# from rest_framework.authentication import 
# Authentication and Permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer
from .judgeUtils import *
# import datetime 
from datetime import datetime 

from .customAuth import *

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError , InvalidToken


class LoginApi(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request, format=None):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token = RefreshToken.for_user(user=user)
            return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)
        
        
        # If user not present in local db
        # Fetch API 
        print("Api Fetch")
        return Response(status=status.HTTP_404_NOT_FOUND)
        

class RegisterApi(viewsets.GenericViewSet,mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes=[IsAuthenticated,IsAdminUser]
    authentication_classes = [SessionAuthentication]


class TeamRegisterApi(viewsets.GenericViewSet,mixins.CreateModelMixin):
    queryset = Team.objects.all()
    serializer_class = TeamRegisterSerializer
    permission_classes=[IsAuthenticated,IsAdminUser]
    authentication_classes = [SessionAuthentication]


# class LoginApiView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             print("USer not found")
#             raise InvalidToken(e.args[0])
           
#         res = Response(serializer.validated_data, status=status.HTTP_200_OK)
#         # access_token = serializer.validated_data['access']
#         return res


def home(request):
    '''To check redirection'''
    codeDict = {
        1:"Redirected After time end",
    }
    return HttpResponse(codeDict[1])

class TimeCheck:
    '''Class to handle time end
    by invoking dispatch method where it is inherited

        contest_time = Contest_time.objects.all()
        end_time = contest_time[0].end_time.astimezone()
        end_time = datetime(year=end_time.year, month=end_time.month, day=end_time.day, hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        final_time = int(end_time.timestamp())   #user end time in sec
        current_time =  int(datetime.now().timestamp())   #crrent server time in sec
        print("end time ",final_time,end_time)
        print("crnt time ",current_time,datetime.now())
        print("diff ",final_time-current_time)
        dif = final_time-current_time
    '''

    
    def dispatch(self, request, *args, **kwargs):
        eventTimeQuery = ContestTime.objects.get(id=1)
        eventEndTime = eventTimeQuery.endTime.astimezone()
        print("Event time => ",eventEndTime)
        endTimeConverted = datetime(year=eventEndTime.year, month=eventEndTime.month, day=eventEndTime.day, hour=eventEndTime.hour, minute=eventEndTime.minute, second=eventEndTime.second)    
        endTime = int(endTimeConverted.timestamp())


        currentTime = int(datetime.now().timestamp())
        print("current timr => ",datetime.now())
        print("*****Time*****")
        print("End time => ",endTime)
        print("Current time => ",currentTime)

        # Check if time is over
        if currentTime > endTime:
            return redirect('/home/')  # Redirect to 'home' 

        return super().dispatch(request, *args, **kwargs)

class QuestionViewSet(TimeCheck,viewsets.ReadOnlyModelViewSet):
    '''
    To get question list respective to category (Junior,Senior,Both)
    To get specific question by question ID from URL
    '''
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field="questionId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        team = Team.objects.get(Q(user1 = user) | Q(user2 = user))
        return queryset.filter(Q(category= "junior" if team.isJunior else "senior" ) | Q(category="both"))  #return  questions filtered with two  conditions


class RatingViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = RatingSerializer(data=data)
        if serializer.is_valid():
            user = self.request.user
            serializer.validated_data["user"] = user
            serializer.save()
        return Response(serializer.data)
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
class LeaderBoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = LeaderBoardSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [LeaderboardJwt]
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        junior_query = Team.objects.filter(isJunior=True).order_by("-score", "lastUpdate")
        senior_query = Team.objects.filter(isJunior=False).order_by("-score", "lastUpdate")

        junior_serializer = LeaderBoardSerializer(junior_query, many=True)
        senior_serializer = LeaderBoardSerializer(senior_query, many=True)

        if user.is_anonymous:
            response_data = {
                'juniorLeaderboard': junior_serializer.data,
                'seniorLeaderboard': senior_serializer.data,
            }
            return Response(response_data)
        else:
            teamQuery = Team.objects.get(Q(user1 = user) | Q(user2 = user))
            teamRank = IndividualLeaderBoardSerializer(teamQuery)

            response_data = {
                'personalRank':teamRank.data,
                'juniorLeaderboard': junior_serializer.data,
                'seniorLeaderboard': senior_serializer.data
            }
            return Response(response_data)
        

class Submit(TimeCheck,viewsets.GenericViewSet,mixins.CreateModelMixin):

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    # def perform_create(self, serializer):


    #     return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():
            user = self.request.user
            team = Team.objects.get(Q(user1 = user) | Q(user2 = user))
            # team = serializer.validated_data['team']

            code = serializer.validated_data['code']
            language = serializer.validated_data['language']
            question = serializer.validated_data['question']

            input = serializer.validated_data.pop('input', "")
            isSubmitted = serializer.validated_data.pop('isSubmitted', False)
            # print(serializer.data)

            if isSubmitted:
                print("*******Valid  and saved*******")
                codeStatus=  runCode(question,code,language,isSubmitted,input)

                # return_code_testcase1 = codeStatus["testcase1"]["returnCode"]    #One method to get rc from runCode 
                # print("Return code of testcase1:", return_code_testcase1)
                
                returnCodeList = []
                for testcase, values in codeStatus.items():
                    returnCodeList.append(values["returnCode"])
                
                print(returnCodeList)
                if (returnCodeList.count(0) == len(returnCodeList)):
                    #It will work when user get all AC submission
                    serializer.validated_data['status'] = ErrorCodes[0]

                    score = self.getMaxScore(question,team)

                    serializer.validated_data['points'] = score
                    serializer.validated_data['isCorrect'] = True

                    lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
                    serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
                    serializer.validated_data['team'] = team
                    serializer.save()

                    #This team query to save users score and last update in score
                    teamQuery= Team.objects.get(teamId = team)
                    teamQuery.score += score
                    teamQuery.lastUpdate = datetime.now()
                    teamQuery.save()
                else:
                    #When answer is other than AC
                    serializer.validated_data['status'] = ErrorCodes[returnCodeList[-1]]
            
                    serializer.validated_data['points'] = 0
                    serializer.validated_data['isCorrect'] = False

                    lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
                    serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
                    serializer.validated_data['team'] = team
                    serializer.save()

                # print(question.questionId)    #to get question id from question 
                
                return Response(codeStatus)
            else:
                print("*******Valid but not saved*******")
                codeStatus=  runCode(question,code,language,isSubmitted,input)
                codeStatus.update(serializer.data)
                responce = codeStatus
                print("responce => ",responce)
                return Response(codeStatus)
        else:
            print("*******Invalid*******")
            # print(request.data)
            return Response({'msg':serializer.errors})
        

    def getMaxScore(self,question,team):
        questionQuery = Question.objects.get(questionId=question.questionId)
        points = questionQuery.points
        maxPoints = questionQuery.maxPoints

        
        try:
            submissionQuery = Submission.objects.filter(team = team ,question = question,isCorrect=True).exists()
            if submissionQuery:
                print("Right submission exits")
                return 0
            else:
                questionQuery.points -=1
                questionQuery.save()
                try:
                    submissionQuery = Submission.objects.filter(team = team ,question = question,isCorrect = False).exists()
                    if submissionQuery:
                        penalty = Submission.objects.filter(team = team ,question = question).last().attemptedNumber
                        
                        score = int(points - (penalty * 0.1 * points))
                        print("points -> ",points,"\n maxpoints -> ",maxPoints)
                        print("penalty -> ",penalty,"\nScore -> ",score)

                        if score > 0:
                            print("score > 0")
                            return score
                        print("score < 0")
                        #User will get 10 points if its score is negative for right submission
                        return 10
                except:
                    print("score = maxpoints")
                    return points
        except:
            pass

    

class GetSubmissions(TimeCheck,viewsets.GenericViewSet,mixins.ListModelMixin):
    '''This view get parameters from url'''
    
    queryset = Submission.objects.all()
    serializer_class = GetSubmissionSerializer
    lookup_field="question"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        team = Team.objects.get(Q(user1 = user)| Q(user2 = user))
        queryset = super().get_queryset()
        queryset = queryset.filter(team = team).order_by("-id")
        

        question = self.request.query_params.get("question")
        if question:    
            print(question)
            queryset = queryset.filter(question=question)
        
            
        return queryset
    
    # http://127.0.0.1:8000/api/submissions/?question=fa152
        

