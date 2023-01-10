from django.shortcuts import render
from .models import *
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AnswerSerializer, MarkSerializer, QuestionSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
  
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        users = get_list_or_404(User, user_score__school__name='ATC')
        return users.order_by('user_score__rank')



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
    #queryset = School.objects.get(name='ATC').questions.all().order_by('category')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self, request):
        school = get_object_or_404(School, name='ATC')
        return school.questions.all().order_by('category')


class AnswerQuestions(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, school, pk, format=None):
        answer = request.POST.get('answer')
        question  = get_object_or_404(Questions, pk=pk)
        # check if enrolled for school
        ans_school = get_object_or_404(School, slug=school)
        # check if question is alrady answered
        mark , created = Mark.objects.get_or_create(user=request.user, question=question, school=ans_school)
        if mark.answered:
            return Response({
                "message": "Question already answered"})
        
        if answer.lower().strip() == question.answer:
            mark.answered =True
            mark.save() 
            right = Mark.objects.filter(question=question, answered=True, school=ans_school)
            serializer = MarkSerializer(right, context={'request': request}, many=True)
            return Response(serializer.data)
        return Response({"message":"Answer is Incorrect"})

