from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Regular Django views for server-side rendering
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('users.urls')),
    path('jobs/', include('jobs.urls')),

    # Keep API endpoints for possible future use
    path('api/', include('users.api_urls')),
    path('api/', include('jobs.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
