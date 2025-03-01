from rest_framework import serializers
from .models import Job, JobApplication
from users.serializers import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Job
        fields = '__all__'

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'deadline', 'max_participants', 'status']

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = JobApplication
        fields = '__all__'

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['message']

class JobApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']
