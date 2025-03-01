from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import Job

def home_view(request):
    """
    Home page view that shows recent jobs
    """
    recent_jobs = Job.objects.all().order_by('-created_at')[:5]

    context = {
        'jobs': recent_jobs
    }

    return render(request, 'home.html', context)

@login_required
def theme_selection_view(request):
    """
    Page for selecting a theme
    """
    return render(request, 'themes/theme_selection.html')
