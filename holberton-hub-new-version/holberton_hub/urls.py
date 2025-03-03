from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import HomeView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages

# Add this function to handle theme selection
def select_theme(request):
    if request.method == 'POST':
        theme = request.POST.get('theme', 'default')
        request.session['theme'] = theme
        messages.success(request, f"Theme changed to {theme}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('users/', include('users.urls')),
    path('jobs/', include('jobs.urls')),
    path('projects/', include('projects.urls')),  # Make sure this line exists
    # Add any other URL includes here

    # Add authentication views from Django
    path('accounts/', include('django.contrib.auth.urls')),

    # Theme selection views
    path('themes/selection/', TemplateView.as_view(
        template_name='themes/theme_selection.html'
    ), name='theme_selection'),
    path('themes/set/', select_theme, name='set_theme'),

    # Comment out or remove the API URLs until we implement them
    # path('api/', include('users.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
