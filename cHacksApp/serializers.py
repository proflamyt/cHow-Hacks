from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Mark, Questions, School, SchoolScore, Notification

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['has_changed_password'] = user.changed_password
        return token

class SchoolSerializer(serializers.Serializer):
    score = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()

    def get_user_score(self, user):
        serializer = SchoolSerializer(user.user_score.get(school__name='ATC'))
        return serializer.data.get("score")

    class Meta:
        model = User
        fields = [ 'username', 'user_score']
       


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    # ans_num = serializers.IntegerField()
    id = serializers.IntegerField()
    class Meta:
        model = Questions
        # fields = ['url', 'id', 'name', 'weight', 'category', 'encoded', 'description', 'file', 'code', 'question_type' ]
        exclude = ('answer',)
    def to_representation(self, instance):
        request = self.context.get('request') 
        ans_school = get_object_or_404(School, name='ATC')
        representation = super().to_representation(instance)
        marked, _ = Mark.objects.get_or_create(user=request.user, question=instance, school=ans_school)
        representation['is_solved'] = marked.answered
        return representation

class MarkSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Mark
        fields = [ 'user']

class NotificationSerializer(serializers.ModelSerializer):
    model = Notification
    exclude = ("user",)


class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField( required=True, validators=[validate_password])


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ("user",)