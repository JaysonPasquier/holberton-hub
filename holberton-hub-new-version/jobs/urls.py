from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('new/', views.JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('<int:pk>/apply/', views.apply_to_job, name='job_apply'),
    path('application/<int:application_id>/<str:action>/', views.manage_application, name='manage_application'),
]
