from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'company', 'is_active', 'created_at']
    list_filter = ['is_active', 'job_type', 'created_at']
    search_fields = ['title', 'company', 'location', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['skills']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['job__title', 'applicant__username', 'applicant__email']
    date_hierarchy = 'applied_at'
    readonly_fields = ['applied_at']
