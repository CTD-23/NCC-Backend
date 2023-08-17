# tasks.py (create this file in your app directory)

from celery import shared_task
from .utils import getContainer, deallocate
from .judgeUtils import *
from .serializers import *
from datetime import datetime 
from rest_framework.response import Response

from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
import json
@shared_task(bind=True)
def homee(self,a):
    print("***************celery request************")
    # return Response({'msg':'doen'})
    # return HttpResponse("done")
    processed_data = {'result': a * 2}

    # Return the JSON data
    return processed_data
    





def getMaxScore(question,team):
    questionQuery = Question.objects.get(questionId=question)
    points = questionQuery.points
    maxPoints = questionQuery.maxPoints
    print("inside get score ",question , team)
    
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
                else:
                    return points
            except:
                print("score = maxpoints")
                return points
    except:
        print("None value is returing ")
        pass




@shared_task(bind=True)
def execute_code_task(self,question, code, language, isSubmitted, container, input_data=None,submissionId = None):
    '''
    runCode(question,code, language,isSubmitted,userId,input=None)
    '''
    try:
        if isSubmitted:
            
            print("*******Valid  and saved*******")
            codeStatus=  runCode(question,code,language,isSubmitted,container,input_data)
            # return_code_testcase1 = codeStatus["testcase1"]["returnCode"]    #One method to get rc from runCode 
            # print("Return code of testcase1:", return_code_testcase1)
            userSubmission = Submission.objects.get(id = submissionId)
            team = Team.objects.get(teamId = userSubmission.team)
            returnCodeList = []
            for testcase, values in codeStatus.items():
                returnCodeList.append(values["returnCode"])
            
            # print(returnCodeList)
            if (returnCodeList.count(0) == len(returnCodeList)):
                #It will work when user get all AC submission
                userSubmission.status = ErrorCodes[0]
                # serializer.validated_data['status'] = ErrorCodes[0]
                score = getMaxScore(question,team)
                # print("************ score ",score )
                userSubmission.points = score
                # serializer.validated_data['points'] = score
                userSubmission.isCorrect = True
                # serializer.validated_data['isCorrect'] = True
                try:
                    lastSubmissionNumber = Submission.objects.filter(question=question,team=team)
                    lastSubmissionNumber = lastSubmissionNumber[len(lastSubmissionNumber) - 2 ]
                    userSubmission.attemptedNumber =  lastSubmissionNumber.attemptedNumber+1
                except:
                    # print("44444444444")
                    userSubmission.attemptedNumber =  1
                    # serializer.validated_data['attemptedNumber'] = 1
                userSubmission.save()
                #This team query to save users score and last update in score
                teamQuery= Team.objects.get(teamId = team)
                teamQuery.score += score
                teamQuery.lastUpdate = datetime.now()
                teamQuery.save()
            else:
                #When answer is other than AC
                userSubmission.status = ErrorCodes[returnCodeList[-1]]
                # serializer.validated_data['status'] = ErrorCodes[returnCodeList[-1]]
        
                userSubmission.points = 0
                # serializer.validated_data['points'] = 0
                userSubmission.isCorrect = False
                # serializer.validated_data['isCorrect'] = False
                lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
                userSubmission.attemptedNumber = lastSubmissionNumber+1
                # serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
                userSubmission.save()
            # print(question.questionId)    #to get question id from question 
            
            return codeStatus
            
        else:
            print("*******Valid but not saved*******")
            codeStatus=  runCode(question,code,language,isSubmitted,container,input_data)
            # codeStatus["input"]=input
            # print(type(codeStatus),"++++++++++++++++++++++")
            # print("responce => ",responce)
            # a = {"dfs":"SDfsdf"}
            return codeStatus
        
    except:
        message = {
            "msg":"Server is Busy"
        }
        return message
