from django.contrib import admin
from .models import Project, ProjectApplication

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'company', 'is_company_project', 'is_paid', 'created_at', 'is_active')
    list_filter = ('is_company_project', 'is_paid', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'company', 'creator__username')
    date_hierarchy = 'created_at'

@admin.register(ProjectApplication)
class ProjectApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'project', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('applicant__username', 'project__title', 'message')
    date_hierarchy = 'applied_at'
