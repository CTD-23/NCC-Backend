from rest_framework import serializers
from .models import *
from django.db.models import Q

class QuestionSerializer(serializers.ModelSerializer):
    solvedByTeam = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"
        extra_fields = ["solvedByTeam"]

    def get_solvedByTeam(self, obj):
        user = self.context['request'].user
        team = Team.objects.get(Q(user1 = user) | Q(user2 = user))

        return Submission.objects.filter(team=team, question=obj, isCorrect=True).exists()


class RatingSerializer(serializers.ModelSerializer):
     class Meta:
        model = Rating
        fields = "__all__"


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
    input = serializers.CharField(default=None)
    # question = serializers.CharField()
    class Meta:
        model = Submission
        fields = ['team','question','language','code','isSubmitted','input']
        extra_fields = ['attemptedNumber','submissionTime','points','status','isCorrect']

class GetSubmissionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Submission
        fields = ['id','team','question','language','code','isCorrect','points','submissionTime','status']