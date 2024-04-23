from rest_framework import serializers
from .models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class CandidateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['status']

class CandidateSearchSerializer(serializers.Serializer):
    min_salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_age = serializers.IntegerField(required=False)
    max_age = serializers.IntegerField(required=False)
    min_exp = serializers.IntegerField(required=False)
    phone_number = serializers.CharField(max_length=15, required=False)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(max_length=100, required=False)