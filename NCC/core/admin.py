from django.contrib import admin
from .models import *


class QuestionAdmin (admin.ModelAdmin):
    list_display = ("questionId","questionNumber","maxPoints","points","title","category")
admin.site.register(Question,QuestionAdmin)

class SubmissionAdmin (admin.ModelAdmin):
    list_display = ('id',"team","question","language","status","isCorrect","submissionTime","points","attemptedNumber")
admin.site.register(Submission,SubmissionAdmin)

class TestcaseAdmin (admin.ModelAdmin):
    list_display = ("question","testcaseNumber")
admin.site.register(Testcase,TestcaseAdmin)

class TeamAdmin (admin.ModelAdmin):
    list_display = ("teamId","user1","user2","score","isJunior","lastUpdate")
admin.site.register(Team,TeamAdmin)

class ContestTimeAdmin (admin.ModelAdmin):
    list_display = ("id","startTime","endTime")
admin.site.register(ContestTime,ContestTimeAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display= ("id","user","rating")
admin.site.register(Rating,RatingAdmin)


