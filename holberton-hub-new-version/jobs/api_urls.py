from django.urls import path
from . import api_views

urlpatterns = [
    path('jobs/', api_views.JobList.as_view(), name='api_job_list'),
    path('jobs/<int:pk>/', api_views.JobDetail.as_view(), name='api_job_detail'),
    path('jobs/create/', api_views.JobCreate.as_view(), name='api_job_create'),
    path('jobs/<int:pk>/update/', api_views.JobUpdate.as_view(), name='api_job_update'),
    path('jobs/<int:pk>/delete/', api_views.JobDelete.as_view(), name='api_job_delete'),
    path('jobs/<int:pk>/applications/', api_views.JobApplicationList.as_view(), name='api_job_application_list'),
    path('jobs/<int:job_id>/apply/', api_views.JobApplicationCreate.as_view(), name='api_job_apply'),
    path('applications/<int:pk>/', api_views.JobApplicationDetail.as_view(), name='api_job_application_detail'),
    path('applications/<int:pk>/status/', api_views.JobApplicationStatusUpdate.as_view(), name='api_job_application_status'),
]
