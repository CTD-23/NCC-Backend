from rest_framework import viewsets
from rest_framework.generics import mixins
from .models import *
from .serializers import *
from django.views import View
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import json,io
from django.db.models import Q 
# from rest_framework.authentication import 
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from .judgeUtils import *
import datetime 


def home(request):
    '''To check redirection'''
    codeDict = {
        1:"Redirected After time end",
    }
    return HttpResponse(codeDict[1])

class TimeCheckMixin:
    '''Class to handle time end
    by invoking dispatch method where it is inherited
    '''
    eventTimeQuery = ContestTime.objects.get(id=1)
    eventEndTime = eventTimeQuery.endTime.astimezone()
    endTimeConverted = datetime.datetime(year=eventEndTime.year, month=eventEndTime.month, day=eventEndTime.day, hour=eventEndTime.hour, minute=eventEndTime.minute, second=eventEndTime.second)    
    endTime = int(endTimeConverted.timestamp())

    
    def dispatch(self, request, *args, **kwargs):
        currentTime = int(datetime.datetime.now().timestamp())
        print("*****Time*****")
        print("End time",self.endTime)
        print("Current time",currentTime)

        # Check if time is over
        if currentTime > self.endTime:
            return redirect('/home/')  # Replace 'home' with the URL name of your home page view

        return super().dispatch(request, *args, **kwargs)

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field="questionId"
    permission_classes = [IsAuthenticated]    

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        team = Team.objects.get(Q(user1 = user) | Q(user2 = user))
        return queryset.filter(Q(category= "junior" if team.isJunior else "senior" ) | Q(category="both"))  #return  questions filtered with two  conditions


class RatingViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
class LeaderBoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = LeaderBoardSerializer
    renderer_classes = [JSONRenderer]

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
        

class Submit(viewsets.GenericViewSet,mixins.CreateModelMixin):

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():
            # user = self.request.user
            # team = Team.objects.get(Q(user1 = user) | Q(user2 = user))
            team = serializer.validated_data['team']

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
                    serializer.save()

                    #This team query to save users score and last update in score
                    teamQuery= Team.objects.get(teamId = team)
                    teamQuery.score += score
                    teamQuery.lastUpdate = datetime.datetime.now()
                    teamQuery.save()
                else:
                    #When answer is other than AC
                    serializer.validated_data['status'] = ErrorCodes[returnCodeList[-1]]
            
                    serializer.validated_data['points'] = 0
                    serializer.validated_data['isCorrect'] = False

                    lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
                    serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
                    serializer.save()

                # print(question.questionId)    #to get question id from question 

                return Response(codeStatus)
            else:
                print("*******Valid but not saved*******")
                codeStatus=  runCode(question,code,language,isSubmitted,input)
                
                return Response(codeStatus)
        else:
            print("*******Invalid*******")
            print(request.data)
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

'''
        contest_time = Contest_time.objects.all()
        end_time = contest_time[0].end_time.astimezone()
        end_time = datetime(year=end_time.year, month=end_time.month, day=end_time.day, hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        final_time = int(end_time.timestamp())   #user end time in sec
        current_time =  int(datetime.now().timestamp())   #crrent server time in sec
        print("end time ",final_time,end_time)
        print("crnt time ",current_time,datetime.now())
        print("diff ",final_time-current_time)
        dif = final_time-current_time'''


    
class GetSubmissions(TimeCheckMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    queryset = Submission.objects.all()
    serializer_class = GetSubmissionSerializer
    lookup_field="id"
    # permission_classes = [IsAuthenticated]    

    def get_queryset(self):
        user = self.request.user
        team = Team.objects.get(Q(user1 = user)| Q(user2 = user))
        queryset = super().get_queryset()
        queryset = queryset.filter(team = team)
            
        # Getting parameters
        question = self.request.query_params.get("question")
        submission_id = self.request.query_params.get("id",None)
        # team = self.request.query_params.get("team")
        
        #Apply filters to the queryset
        if question:
            queryset = queryset.filter(question=question)
        # if team:
        #     queryset = queryset.filter(team=team)
        if submission_id:
            queryset = queryset.filter(id=submission_id)
            
            

        return queryset
    
    # http://127.0.0.1:8000/api/submissions/?question=fa152&team=232fa&id=4
        

