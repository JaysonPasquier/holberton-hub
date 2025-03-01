from django.urls import path
from . import api_views

urlpatterns = [
    path('users/', api_views.UserList.as_view(), name='api_user_list'),
    path('users/<str:username>/', api_views.UserDetail.as_view(), name='api_user_detail'),
    path('users/<str:username>/update/', api_views.UserUpdate.as_view(), name='api_user_update'),
    path('register/', api_views.RegisterView.as_view(), name='api_register'),
    path('current-user/', api_views.CurrentUserView.as_view(), name='api_current_user'),
]
