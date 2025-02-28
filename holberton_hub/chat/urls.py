from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rooms', views.ChatRoomViewSet)
router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('project/<int:project_id>/', views.project_chat, name='project_chat'),
    path('chatbot/', views.ChatBotViewSet.as_view({'post': 'create'}), name='chatbot'),
] + router.urls
