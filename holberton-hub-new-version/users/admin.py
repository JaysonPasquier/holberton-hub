from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('bio', 'profile_pic', 'skills', 'github_url', 'linkedin_url', 'website')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Optional Fields', {'fields': ('first_name', 'last_name', 'email')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
