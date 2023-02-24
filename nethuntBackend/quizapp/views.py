from django.shortcuts import render
from .models import Info,Quiz
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from user.models import (Coordinator,NethuntUser)
from user.serializers import (CoordinatorSerializer)
from user.serializers import NethuntUserSerializer
from quizapp.models import Info,Question,Progress,CurrentStatus
from .serializers import QuestionSerializer,QuizSerializer
import json
import copy
from datetime import datetime
import requests
import base64

@api_view(["GET"])
def get_startDate(req):
    if (Info.objects.all().count() >= 1):
        return Response({"configured": True,"startDateTime":Info.objects.all()[0].startBy})
    return Response({"configured": False})

@api_view(["GET"])
def get_endDate(req):
    return Response({"configured": True,"endDateTime":Info.objects.all()[0].endBy})



@api_view(["POST"])
def get_log(req):
    url = "https://discord.com/api/webhooks/1077878410271019008/vwKfxy-5NL8az1_Xwlf6zwpWQ0B18hAzUj03wqJU9t8mjs5H3RZ7ZVTo7DUQTQOLB9jA" # Replace with your own webhook URL
    message = "Hello, world!" # Replace with your own message

    payload = {
        "content": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 204:
        return Response({"info":"Message sent to Discord channel."})
    else:
        return Response({"info":"Failed to send message to Discord channel."})

@api_view(["POST"])
def get_quiz_status(req):
    data = json.loads(req.body)
    current_status = CurrentStatus.objects.filter(usr=NethuntUser.objects.get(email=data["email"]),quiz=Quiz.objects.get(name=data["quiz"]))
    if current_status.count() == 0:
        CurrentStatus(usr=NethuntUser.objects.get(email=data["email"]),quiz=Quiz.objects.get(name=data["quiz"])).save()
        Progress(usr==NethuntUser.objects.get(email=data["email"]),quiz=Quiz.objects.get(name=data["quiz"])).save()
        question = Question.objects.all()[current_status[0].level]
        questionSerializer = QuestionSerializer(question,).data
        return Response({"problem":False,"question":questionSerializer})
    elif current_status.count() == 1:
        progress = Progress.objects.filter(usr=NethuntUser.objects.get(email=data["email"]),quiz=Quiz.objects.get(name=data["quiz"]),level=current_status[0].level)
        if progress.count() == 0:
            Progress(usr=NethuntUser.objects.get(email=data["email"]),quiz=Quiz.objects.get(name=data["quiz"]),level=current_status[0].level).save()
            if current_status[0].level + 1 > Question.objects.all().count():
                return Response({"problem":True,"end":True,"multipleCurrentStatus":False,"multipleProgress":False})    
            else:
                question = Question.objects.all()[current_status[0].level]
                questionSerializer = QuestionSerializer(question,).data
                return Response({"problem":False,"question":questionSerializer})
        elif progress.count() == 1:
            question = Question.objects.all()[current_status[0].level]
            # print(question.image.read())
            questionSerializer = QuestionSerializer(question,).data
            questionSerializer["image"] = base64.b64encode(question.image.read()).decode('utf-8')
            return Response({"problem":False,"question":questionSerializer})
        else :
            return Response({"problem":True,"end":False,"multipleCurrentStatus":False,"multipleProgress":True})
    else:
        return Response({"problem":True,"end":False,"multipleCurrentStatus":True,"multipleProgress":False})
    print(progress)
    return Response({"test":"testing"})
@api_view(["GET"])
@permission_classes([IsAdminUser])
def is_configured(req):
    if (Info.objects.all().count() >= 1):
        return Response({"configured": True})
    return Response({"configured": False})

@api_view(["GET"])
def get_questions(req):
    return Response({"data": QuestionSerializer(Question.objects.all(),many=True).data})

@api_view(["POST"])
def add_question(req):
    try:
        data = json.loads(req.POST["data"])
        # print(req.FILES)
        quiz = Quiz.objects.get(name=data["quiz"])
        question = Question(answer=data["answer"],hint1=data["hint1"],hint2=data["hint2"],difficulty=data["difficultyLevel"],quiz=quiz,image=req.FILES["question"])
        question.save()
        return Response({"added":True})
    except:
        return Response({"added":False})
@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_config(req):
    # print(req.FILES[])
    try:
        data = json.loads(req.POST["data"])
        coordinators = data["coordinators"]
        for index, coordinator in zip(range(len(coordinators)), coordinators):
            user = {
                "email": coordinator["coordinatorEmail"],
                "password": coordinator["coordinatorPassword"],
                "first_name": coordinator["coordinatorFirstName"],
                "last_name": coordinator["coordinatorLastName"],
                "role": "Coordinator"
            }
            user = NethuntUserSerializer(data=user)
            if user.is_valid():
                tempUser = user.save()
                coordinator = Coordinator(user=tempUser,image = req.FILES["coordinator"+str(index+1)],phone= coordinator["coordinatorPhone"])
                coordinator.save()
            else:
                NethuntUser.objects.fetch(role="Coordinator").delete()
                return Response({"configured": False})   
        storedCoordinators = Coordinator.objects.all()
        if  storedCoordinators.count()== 2:
            
            eventInfo = data["eventInfo"]
            event = eventInfo["event"]
            year = int(eventInfo["year"])
            commonMailId = eventInfo["commonMailId"] 

            eventLogo = req.FILES["event"]  
            logo = req.FILES["nethunt"]
            
            coordinator1 = storedCoordinators[0]
            coordinator2 = storedCoordinators[1]

            timings = data["quizTimings"]
            startBy = datetime.strptime(timings["startsBy"], '%Y-%m-%dT%H:%M')
            endBy = datetime.strptime(timings["endsBy"], '%Y-%m-%dT%H:%M')

            scorings = data["quizScores"]
            easyScore = int(scorings["easy"])
            moderateScore = int(scorings["medium"])
            hardScore = int(scorings["hard"])
            
            practiceQuiz = Quiz(name="practice")
            practiceQuiz.save()
            practice = Quiz.objects.get(name="Practice")
            mainQuiz = Quiz(name="main")
            mainQuiz.save()
            main = Quiz.objects.get(name="Main")
            print(main,practice)
            data = Info(event=event,year=year,coordinator1=coordinator1,coordinator2=coordinator2,startBy=startBy,endBy=endBy,easyScore=easyScore,moderateScore=moderateScore,hardScore=hardScore,commonMailId=commonMailId,practiceQuiz=practice,mainQuiz=main)
            data.save()
            return Response({"configured": True})
        else:
            NethuntUser.objects.fetch(role="Coordinator").delete()
            Quiz.objects.all().delete()
            return Response({"configured": False}) 
    except:
        NethuntUser.objects.fetch(role="Coordinator").delete()
        Quiz.objects.all().delete()
    return Response({"configured": False})
