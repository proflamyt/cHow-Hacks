from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Mark, Questions, SchoolScore

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['has_changed_password'] = user.changed_password
        return token

class SchoolSerializer(serializers.Serializer):
    score = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()

    def get_user_score(self, user):
        serializer = SchoolSerializer(user.user_score.get(school__name='ATC'))
        print(serializer.data)
        return serializer.data

    class Meta:
        model = User
        fields = [ 'username', 'email', 'user_score']
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
        fields = [ 'user']



class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField( required=True, validators=[validate_password])