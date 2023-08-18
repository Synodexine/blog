from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['user_email', 'text']


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=256)


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=512)


class TokenVerificationSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=512)