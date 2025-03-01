from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, theme_selection_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Regular Django views for server-side rendering
    path('', home_view, name='home'),
    path('users/', include('users.urls')),
    path('jobs/', include('jobs.urls')),
    path('themes/', theme_selection_view, name='theme_selection'),

    # Keep API endpoints for possible future use
    path('api/', include('users.api_urls')),
    path('api/', include('jobs.api_urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
