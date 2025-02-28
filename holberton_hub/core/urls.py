from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import (
    UserViewSet, UserRegisterView, UserUpdateView,
    profile_view, user_profile_view, register
)
from projects.views import (
    ProjectViewSet, ProjectListView, ProjectDetailView,
    ProjectCreateView, application_status, project_apply,
    archive_project, like_project, vote_project  # Ajout de like_project et vote_project
)
from chat.views import ChatRoomViewSet, MessageViewSet, project_chat, ChatBotViewSet
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.conf import settings
from django.conf.urls.static import static
from .views import LandingPageView  # Ajouter cet import

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'chatrooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'chatbot', ChatBotViewSet, basename='chatbot')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Landing page
    path('', LandingPageView.as_view(), name='landing'),

    # Projects URLs
    path('projects/', include('projects.urls')),  # Utiliser l'inclusion des URLs de projects

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/login.html',
                                    next_page='login',
                                    extra_context={'hide_navbar': True}), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', UserUpdateView.as_view(), name='profile_edit'),
    path('user/<str:username>/', user_profile_view, name='user_profile'),

    # API URLs
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),

    # Include other apps URLs
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
