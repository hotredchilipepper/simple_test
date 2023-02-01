from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    #hash_pass = serializers.CharField(max_length=254)
    timestamp_create = serializers.DateTimeField()


class QuestionSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    question = serializers.CharField(max_length=254)
    answer = serializers.CharField(max_length=254)
    timestamp_create = serializers.DateTimeField()