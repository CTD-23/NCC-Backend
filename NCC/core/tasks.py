# tasks.py (create this file in your app directory)

from celery import shared_task
from .utils import getContainer, deallocate
from .judgeUtils import *
from .serializers import *

from rest_framework.response import Response

from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
@shared_task(bind=True)
def homee(self):
    print("***************celery request************")
    # return Response({'msg':'doen'})
    # return HttpResponse("done")
    while 1:
        pass
    processed_data = {'result': 6 * 2}

    # Return the JSON data
    return processed_data
    





def getMaxScore(question,team):
    questionQuery = Question.objects.get(questionId=question.questionId)
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

@shared_task
def execute_code_task(serializer,team,question, code, language, isSubmitted, container, input_data):
    try:
        if isSubmitted:
            print("*******Valid  and saved*******")
            codeStatus=  runCode(question,code,language,isSubmitted,container,input)
            deallocate(container)
            # return_code_testcase1 = codeStatus["testcase1"]["returnCode"]    #One method to get rc from runCode 
            # print("Return code of testcase1:", return_code_testcase1)
            
            returnCodeList = []
            for testcase, values in codeStatus.items():
                returnCodeList.append(values["returnCode"])
            
            # print(returnCodeList)
            if (returnCodeList.count(0) == len(returnCodeList)):
                #It will work when user get all AC submission
                
                serializer.validated_data['status'] = ErrorCodes[0]
                score = getMaxScore(question,team)
                # print("************ score ",score )
                serializer.validated_data['points'] = score
                serializer.validated_data['isCorrect'] = True
                try:
                    lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
                    serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
                except:
                    serializer.validated_data['attemptedNumber'] = 1
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
            codeStatus=  runCode(question,code,language,isSubmitted,container,input)
            deallocate(container)
            serializer.validated_data['input'] = input
            codeStatus.update(serializer.data)
            responce = codeStatus
            # print("responce => ",responce)
            return Response(codeStatus)
        
    finally:
        deallocate(container)
