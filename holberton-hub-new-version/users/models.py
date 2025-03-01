from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from cloudinary.models import CloudinaryField
import cloudinary
import json

# Initialize Cloudinary
cloudinary.config(
    cloud_name = "dsvolcznm",
    api_key = "445719466135631",
    api_secret = "6e_FbbsVgoZi8SyybxHPfzgL8nE",
    secure = True
)

class CustomUser(AbstractUser):
    """Custom user model with additional fields"""
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = CloudinaryField('profile_pic', blank=True, null=True,
                                  folder='profile_pics',
                                  transformation=[
                                      {'width': 300, 'height': 300, 'crop': 'fill'}
                                  ])
    # Original skills field for backward compatibility
    skills = models.TextField(blank=True, help_text="Comma separated list of skills (deprecated)")

    # JSON fields to store skills as lists
    skills_known = models.TextField(blank=True, default='[]',
                              help_text="JSON list of skills the user knows and can teach")
    skills_to_learn = models.TextField(blank=True, default='[]',
                                 help_text="JSON list of skills the user wants to learn")

    # Professional platforms
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")
    website = models.URLField(blank=True, verbose_name="Personal Website")
    stackoverflow_url = models.URLField(blank=True, verbose_name="Stack Overflow URL")
    devto_url = models.URLField(blank=True, verbose_name="Dev.to URL")
    medium_url = models.URLField(blank=True, verbose_name="Medium URL")

    # Social platforms
    twitter_url = models.URLField(blank=True, verbose_name="Twitter/X URL")
    discord_username = models.CharField(max_length=100, blank=True, verbose_name="Discord Username")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram URL")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube URL")
    twitch_url = models.URLField(blank=True, verbose_name="Twitch URL")
    mastodon_url = models.URLField(blank=True, verbose_name="Mastodon URL")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.username)])

    def get_skills_known_list(self):
        """Returns the list of skills the user knows"""
        try:
            return json.loads(self.skills_known)
        except:
            return []

    def get_skills_to_learn_list(self):
        """Returns the list of skills the user wants to learn"""
        try:
            return json.loads(self.skills_to_learn)
        except:
            return []

    def set_skills_known(self, skills_list):
        """Sets the list of skills the user knows"""
        if isinstance(skills_list, list):
            self.skills_known = json.dumps(skills_list)
        else:
            self.skills_known = '[]'

    def set_skills_to_learn(self, skills_list):
        """Sets the list of skills the user wants to learn"""
        if isinstance(skills_list, list):
            self.skills_to_learn = json.dumps(skills_list)
        else:
            self.skills_to_learn = '[]'
