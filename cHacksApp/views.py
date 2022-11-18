from django.shortcuts import render
from .models import *

# Create your views here.


def submit(request, question):
    if request.POST:
        la = request.POST
        user_mark, _ = Mark.objects.get_or_create(user = request.user, question= question)
        if user_mark.answered:
            return {
                "message": "Question already answered"
            }
        elif user_mark.question.answer == la.lower().strip():
            user_mark.answered = True
            user_mark.save()
        
        return {

            "message": "Wrong Answer"
        }

    return Questions.objects.get(id = question)




def questions(request):
    return Questions.objects.all().defer("answer")


def ranking(request):
    users = User.objects.order_by('score')
    return {
        'user':users
    }