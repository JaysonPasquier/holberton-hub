from rest_framework import serializers
from .models import Project, Candidature  # Changer Application en Candidature
from users.serializers import UserSerializer

class CandidatureSerializer(serializers.ModelSerializer):  # Renommer la classe
    applicant = UserSerializer(read_only=True)

    class Meta:
        model = Candidature
        fields = ['id', 'projet', 'candidat', 'message', 'statut', 'date_creation']
        read_only_fields = ['id', 'date_creation']

class ProjectSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    applications = CandidatureSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
