from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import Mark, Questions

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']
        #lookup_field = 'username'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Questions
        fields = ['url', 'name', 'weight', 'category', 'description', 'file', 'code', 'question_type' ]


class MarkSerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='answers', lookup_field='pk')
    user = UserSerializer()
    class Meta:
        model = Mark
        fields = [ 'user', 'question', 'answered']



class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField( required=True, validators=[validate_password])