from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import json
from .skills_constants import SKILL_CHOICES

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

class SkillsField(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        from .skills_constants import SKILL_CHOICES
        kwargs['choices'] = SKILL_CHOICES
        kwargs['required'] = False
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, str):
            try:
                # Parse JSON and ensure we get complete strings
                parsed = json.loads(value)
                if isinstance(parsed, str):
                    return [parsed]
                return parsed
            except (json.JSONDecodeError, TypeError):
                return []
        return value

    def clean(self, value):
        if not value:
            return []
        if isinstance(value, str):
            return [value]
        return value

class CustomUserChangeForm(UserChangeForm):
    password = None
    skills_known = forms.MultipleChoiceField(
        choices=SKILL_CHOICES,
        required=False,
        label='Skills I Know & Can Teach',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'})
    )
    skills_to_learn = forms.MultipleChoiceField(
        choices=SKILL_CHOICES,
        required=False,
        label='Skills I Want to Learn',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'})
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'bio', 'profile_pic',
                 'skills_known', 'skills_to_learn',
                 'github_url', 'linkedin_url', 'stackoverflow_url',
                 'devto_url', 'medium_url', 'website',
                 'twitter_url', 'discord_username', 'instagram_url',
                 'facebook_url', 'youtube_url', 'twitch_url', 'mastodon_url')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # Professional platforms
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.linkedin.com/in/username'
            }),
            'stackoverflow_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://stackoverflow.com/users/123456/username'
            }),
            'devto_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://dev.to/username'
            }),
            'medium_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://medium.com/@username'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com'
            }),
            # Social platforms
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/username'
            }),
            'discord_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username#0000'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.instagram.com/username'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.facebook.com/username'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/@channelname'
            }),
            'twitch_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.twitch.tv/username'
            }),
            'mastodon_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://mastodon.social/@username'
            }),
        }