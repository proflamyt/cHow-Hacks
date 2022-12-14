from django.shortcuts import render
from .models import *
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AnswerSerializer, MarkSerializer, QuestionSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
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



class Certificate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # check if all questions answered
        count_q = Questions.objects.all().count()
        count_a = Mark.objects.filter(user=request.user, answered=True).count()
        if count_q == count_a:
            return Response ({"message":f"congratulations {request.user.name}"})
        return Response({
            "message": "answer all questions"
        })









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
        
        if answer.lower().strip() == question.answer:
            mark.answered =True
            mark.save() 
            right = Mark.objects.filter(answered=True)
            serializer = MarkSerializer(right, context={'request': request}, many=True)
            return Response(serializer.data)
        return Response({"message":"Answer is Incorrect"})

