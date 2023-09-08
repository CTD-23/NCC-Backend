from rest_framework import serializers
from .models import *
from django.db.models import Q

from django.contrib.auth import authenticate
from rest_framework import serializers
# from .models import Result

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                # raise serializers.ValidationError('Invalid username or password.')
                attrs['user'] = None

            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        return attrs

class QuestionSerializer(serializers.ModelSerializer):
    solvedByTeam = serializers.SerializerMethodField()
    accuracy = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = "__all__"
        extra_fields = ["solvedByTeam","accuracy"]
    def get_solvedByTeam(self, obj):
        user = self.context['request'].user
        team = Team.objects.get(Q(user1 = user) | Q(user2 = user))

        return Submission.objects.filter(team=team, question=obj, isCorrect=True).exists()
        
    def get_accuracy(self,obj):
        submissions = Submission.objects.filter(question = obj)
        
        actual_sub = len(submissions)
        right_sub=len(submissions.filter(isCorrect=True))
        try:
            accuracy = round((right_sub/actual_sub)*100)
        except:
            accuracy = 0

        return accuracy
        


class RatingSerializer(serializers.ModelSerializer):
     user = serializers.CharField(required = False)
     rating = serializers.IntegerField()
     class Meta:
        model = Rating
        fields = ["id","user","rating","feedBack"]


class IndividualLeaderBoardSerializer(serializers.ModelSerializer):
    '''
    this serializer gives leaderboard 
    with questions score 
    this serializer gives all player's required queryset
    in leaderboard api it get sorted accordingly 
    '''
    questionSolvedByUser = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    user1 = serializers.CharField()
    user2 = serializers.CharField()
    class Meta:
        model = Team
        fields = ('teamId','user1','user2','score', 'lastUpdate', 'questionSolvedByUser','rank')

    def get_questionSolvedByUser(self, obj):
        # user = self.context['request'].user
        questionQueryset = Question.objects.filter(Q(category= "junior" if obj.isJunior else "senior" ) | Q(category="both"))  #return  questions filtered with two same conditions
        QDict = {}
        submissionQueryset = Submission.objects.filter(isCorrect  = True,team=obj)
        i=1
        for question in questionQueryset:
            try:
                q = submissionQueryset.filter(question = question.questionId , points__gte=0).last()
                QDict[f"Q{i}"]=q.points
            except:
                QDict[f"Q{i}"]=0
            i+=1

        return QDict
    
    def get_rank(self,obj):
        queryset = Team.objects.filter(isJunior=obj.isJunior).order_by('-score', 'lastUpdate')
        ranked_queryset = list(enumerate(queryset, start=1))  # Enumerate the queryset with ranks

        for rank, player in ranked_queryset:
            if player.teamId == obj.teamId:  # Find the player in the ranked queryset
                return rank

        return None
    

class LeaderBoardSerializer(IndividualLeaderBoardSerializer):
    class Meta:
        model = Team
        fields = ('teamId','user1','user2','score', 'lastUpdate', 'questionSolvedByUser','rank')


class SubmissionSerializer(serializers.ModelSerializer):
    isSubmitted  = serializers.BooleanField(default=False)
    # input = serializers.CharField()
    input = serializers.CharField(required = False,default="")
    # question = serializers.CharField()
    class Meta:
        model = Submission
        fields = ['question','language','code','isSubmitted','input']
        extra_fields = ["team",'attemptedNumber','submissionTime','points','status','isCorrect']
        optional_fields = ['input' ]

class GetSubmissionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Submission
        fields = ['id','team','question','language','code','isCorrect','points','submissionTime','status']


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password1 = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('username','password', 'password1','email','first_name', 'last_name')
        extra_kwargs = {

            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Password fields didn't match For user ."})
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class TeamRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['user1','user2','isJunior']
        extra_kwargs = {
            'score': {'required': False},
            'lastUpdate': {'required': False},
        }
    

class GetTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestTime
        fields = "__all__"

# class ResultSerializer(serializers.ModelSerializer):
#     teamId =serializers.CharField(max_length=10, editable=False)
#     isLogin = serializers.BooleanField(default=False)
#     score = serializers.IntegerField(default=0)
#     isJunior = serializers.BooleanField(default=True)
#     questions_attempted = serializers.IntegerField(default=0)
#     questions_solved = serializers.IntegerField(default=0)

#     class Meta :
#         model = Result
#         field= ('teamId','score','questions_attempted','questions_solved')
    