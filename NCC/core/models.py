from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
# from tinymce import TinyMCE
from tinymce import models as mc


# Question model
class Question(models.Model):
    questionId = models.CharField(max_length=10,primary_key=True,editable=False)
    questionNumber = models.IntegerField(unique=True)

    title =models.CharField(max_length=100)
    description = mc.HTMLField()
    
    ipFormate = mc.HTMLField()
    opFormate = mc.HTMLField()

    constraints = mc.HTMLField(null=True,blank=True)

    inputOutputBlock = mc.HTMLField(null=True)

    sampleIp = models.TextField(null=True,blank=True)
    sampleOp = models.TextField(null=True,blank=True)
    
    difficultyLevel = models.IntegerField(default=0)
    maxPoints = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    timeLimit = models.IntegerField(default=1)
    memoryLimit = models.IntegerField(default=524288)
    
    accuracy = models.IntegerField(default=0)
    totalSubmissions = models.IntegerField(default=0)
    author = models.CharField(max_length=100,default="")

    category_choice= [("junior","junior"),("senior","senior"),("both","both")]
    category = models.CharField(choices=category_choice, max_length=10,null=True)
    
    def save(self,*args, **kwargs):
        if not self.questionId:
            self.questionId = str(uuid.uuid4())[:5]
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.questionNumber)

#Testcases
def getIpPath(instance,filename):
    return str(f"testcases/question{instance.question}/input/{filename}")
def getOpPath(instance,filename):
    return str(f"testcases/question{instance.question}/output/{filename}")

class Testcase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    testcaseNumber = models.IntegerField()  
    inputFile = models.FileField( upload_to=getIpPath, blank=True,verbose_name="Testcase Input")
    outputFile = models.FileField( upload_to=getOpPath, blank=True,verbose_name="Testcase Output") 
    def __str__(self):
        return f"{self.question}"
    
#Team
class Team(models.Model):
    teamId = models.CharField(max_length=10, primary_key=True, editable=False)
    user1 = models.OneToOneField(User, related_name="user1", on_delete=models.CASCADE)
    user2 = models.OneToOneField(User, related_name="user2", on_delete=models.CASCADE,blank=True,null=True)
    isLogin = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    isJunior = models.BooleanField(default=True)
    lastUpdate = models.DateTimeField(default=datetime.datetime.now())

    def save(self, *args, **kwargs):
        if not self.teamId:
            self.teamId = str(uuid.uuid4())[:5]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.teamId}"



class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    
    languageChoice = (
        ('python','python'),
        ('cpp','cpp'),
        ('c','c'),
    )
    language = models.CharField(choices=languageChoice,max_length=10)
    code = models.TextField(null=True,blank=True)
    points = models.IntegerField(default=0)
    attemptedNumber = models.IntegerField(default=0)
    submissionTime= models.DateTimeField(auto_now_add=True)

    statusChoice = (
        ('TLE','Time Limit Exceeded'),
        ('MLE','Memory Limit Exceeded'),
        ('CE','Compilation Error'),
        ('RE','Runtime Error'),
    	('WA','Wrong Answer'), 	
        ('AC' ,'Accepted'),
        ('PEN',"Pending")
    )
    status = models.CharField(max_length=5,choices=statusChoice,blank=True,null=True)
    isCorrect = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team}"
    
class ContestTime(models.Model):
    startTime = models.DateTimeField(blank=True)
    endTime = models.DateTimeField(blank=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    feedBack = models.TextField()

    def __str__(self) -> str:
        return str(self.user)

'''
Player model for supervision
use if necessory
'''
# class Player(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     teamId = models.OneTOOneField(Team, on_delete=models.CASCADE)
#     loginCount= models.IntegerField(default=0)
#     isStarted = models.BooleanField(default=False)
#     isLogedIn = models.BooleanField(default=False)
#     startTime = models.DateTimeField(null=True,blank=True)    
#     def __str__(self):
#         return f"{self.user}"


class Container(models.Model):
    containerId = models.IntegerField()
    status = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

# class Result(models.Model):
#     teamId = models.CharField(max_length=10, primary_key=True, editable=False)
#     isLogin = models.BooleanField(default=False)
#     score = models.IntegerField(default=0)
#     isJunior = models.BooleanField(default=True)
#     questions_attempted = models.IntegerField(default=0)
#     questions_solved = models.IntegerField(default=0)

