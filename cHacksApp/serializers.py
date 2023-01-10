from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Mark, Questions

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Questions
        fields = ['url', 'name', 'weight', 'category', 'description', 'file', 'code', 'question_type' ]


class MarkSerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='answers', lookup_field='pk')
    class Meta:
        model = Mark
        fields = [ 'user', 'question', 'answered']



class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()