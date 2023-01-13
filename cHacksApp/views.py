from .models import *
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AnswerSerializer, MarkSerializer, PasswordSerializer, QuestionSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status

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
        return users



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

    def get_queryset(self):
        school = get_object_or_404(School, name='ATC')
        return school.questions.all().order_by('category')


class AnswerQuestions(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, school='ATC', pk=1, format=None):
        try:
            answer = request.data.get('answer')
            question  = get_object_or_404(Questions, pk=pk)
            # check if enrolled for school
            print(School.objects.all().values())
            ans_school = get_object_or_404(School, name=school)
            
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
            return Response({"message":"Answer is Incorrect" }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"Bad Request" }, status=status.HTTP_400_BAD_REQUEST)



class PasswordChange(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordSerializer

    def put(self, request):
        serializer = PasswordSerializer(data=request.data)
       
        if serializer.is_valid(raise_exception=True):
            request.user.set_password(serializer.data.get('password'))
            request.user.save()
            return Response({
                "message": "Password Changed Successfully", 
            },status=status.HTTP_201_CREATED)
        return Response({"message": ["Invalid Password"]}, status=status.HTTP_400_BAD_REQUEST)   

