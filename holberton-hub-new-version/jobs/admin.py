from django.contrib import admin
from .models import Job, JobApplication

class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    readonly_fields = ['applied_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [JobApplicationInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If not superuser, only show own jobs
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'applied_at', 'status']
    list_filter = ['status', 'applied_at']
    search_fields = ['job__title', 'applicant__username', 'message']
    readonly_fields = ['applied_at']
