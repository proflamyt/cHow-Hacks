from django.shortcuts import render
from .models import *
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AnswerSerializer, MarkSerializer, QuestionSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('rank')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']


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








class QuestionsView(viewsets.ModelViewSet):
    """
    Returns all Questions 
    """
    queryset = Questions.objects.all().order_by('category')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']


class AnswerQuestions(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk, format=None):
        answer = request.POST.get('answer')
        question  = get_object_or_404(Questions, pk=pk)
        # check if question is alrady answered
        mark , created = Mark.objects.get_or_create(user=request.user, question=question)
        if mark.answered:
            return Response({
                "message": "Question already answered"})
        
        if answer == question.answer:
            mark.answered =True
            mark.save() 
            right = Mark.objects.filter(answered=True)
            serializer = MarkSerializer(right, context={'request': request}, many=True)
            return Response(serializer.data)
        return Response({"message":"Answer is Incorrect"})

