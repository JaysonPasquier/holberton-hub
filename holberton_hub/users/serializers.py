from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture', 'profile_picture_url', 'specialty', 'last_activity']

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return "https://res.cloudinary.com/dsvolcznm/image/upload/v1/profile_pictures/default_avatar.png"
