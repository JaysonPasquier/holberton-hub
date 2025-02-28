from django.urls import path
from . import views
from .views import ProjectUpdateView

urlpatterns = [
    # Les URLs de like et vote doivent être avant l'URL du détail pour éviter les conflits
    path('<int:pk>/like/', views.like_project, name='like_project'),
    path('<int:pk>/vote/', views.vote_project, name='vote_project'),
    path('new/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('application/<int:pk>/status/', views.application_status, name='application_status'),
    path('<int:pk>/apply/', views.project_apply, name='project_apply'),
    path('<int:pk>/archive/', views.archive_project, name='archive_project'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('', views.ProjectListView.as_view(), name='project_list'),
]
