from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import cloudinary
import json
import logging
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .cloudinary_init import initialize_cloudinary
from .skills_constants import SKILL_CHOICES, SKILL_COLORS

# Ensure Cloudinary is initialized
initialize_cloudinary()

# Set up logging
logger = logging.getLogger(__name__)

User = get_user_model()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SKILL_CHOICES'] = SKILL_CHOICES
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/profile_edit.html'

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET' and self.object:
            # For GET requests, prepare the skills data for the form
            try:
                skills_known = json.loads(self.object.skills_known)
            except:
                skills_known = []

            try:
                skills_to_learn = json.loads(self.object.skills_to_learn)
            except:
                skills_to_learn = []

            initial = kwargs.get('initial', {})
            initial.update({
                'skills_known': skills_known,
                'skills_to_learn': skills_to_learn,
            })
            kwargs['initial'] = initial
        return kwargs

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        # Make sure we're using the Cloudinary configuration
        initialize_cloudinary()

        # Handle the skills fields separately
        skills_known = self.request.POST.getlist('skills_known')
        skills_to_learn = self.request.POST.getlist('skills_to_learn')

        # Set the skills on the user modely
        user = form.save(commit=False)
        user.skills_known = json.dumps(skills_known)
        user.skills_to_learn = json.dumps(skills_to_learn)
        return super().form_valid(form)

class HomeView(TemplateView):
    """View for the homepage."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data you want to pass to the homepage template
        # For example, recent jobs and projects
        from jobs.models import Job
        from projects.models import Project

        context['recent_jobs'] = Job.objects.filter(is_active=True).order_by('-created_at')[:5]
        context['recent_projects'] = Project.objects.filter(is_active=True).order_by('-created_at')[:5]
        return context

class ThemeSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'users/theme_selection.html'

    def post(self, request, *args, **kwargs):
        theme = request.POST.get('theme', 'light')
        # In a real implementation, you'd save this to the user's profile
        # For now, just show a message
        messages.success(request, f"Theme changed to {theme}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Add this signup function that's referenced in urls.py
def signup(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

# View profile - can be your own or another user's
def profile_view(request, username=None):
    """Display a user profile."""
    # If username is provided, get that user's profile
    # If not, display the current user's profile
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        # If not logged in & no username specified, redirect to login
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to view your profile.')
            return redirect('login')
        profile_user = request.user

    # Get user's projects if applicable
    user_projects = []
    if hasattr(profile_user, 'projects'):
        user_projects = profile_user.projects.all()

    # Debug the skills data
    skills_known = []
    if profile_user.skills_known:
        try:
            skills_known = json.loads(profile_user.skills_known)
            logger.info(f"Skills known: {skills_known}")
        except json.JSONDecodeError:
            logger.error(f"Failed to parse skills_known: {profile_user.skills_known}")

    skills_to_learn = []
    if profile_user.skills_to_learn:
        try:
            skills_to_learn = json.loads(profile_user.skills_to_learn)
            logger.info(f"Skills to learn: {skills_to_learn}")
        except json.JSONDecodeError:
            logger.error(f"Failed to parse skills_to_learn: {profile_user.skills_to_learn}")

    # Add skill colors as JSON for the template
    skill_colors_json = json.dumps(SKILL_COLORS)

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'user_projects': user_projects,
        'skill_colors_json': skill_colors_json,
        'skill_choices': SKILL_CHOICES,
        'skill_colors': json.dumps(SKILL_COLORS)
    })

# Edit profile - only available to the logged-in user
@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Get the skills directly
            skills_known = request.POST.getlist('skills_known')
            skills_to_learn = request.POST.getlist('skills_to_learn')

            print(f"Raw skills_known: {skills_known}")

            # Force each skill to be a single complete string, not parsed into characters
            # This is critical to prevent character-by-character storage
            user.skills_known = json.dumps([str(s) for s in skills_known])
            user.skills_to_learn = json.dumps([str(s) for s in skills_to_learn])

            user.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        initial_data = {}

        # Parse existing skills correctly - need to make sure these are usable in the template
        try:
            # Get skills as the proper Python objects (not JSON strings)
            skills_known_raw = json.loads(request.user.skills_known or '[]')
            skills_to_learn_raw = json.loads(request.user.skills_to_learn or '[]')

            # Make them available to the template directly
            context_user_skills = {
                'skills_known': skills_known_raw,
                'skills_to_learn': skills_to_learn_raw
            }

            # Also set up for the form
            initial_data['skills_known'] = skills_known_raw
            initial_data['skills_to_learn'] = skills_to_learn_raw

        except (json.JSONDecodeError, TypeError):
            skills_known_raw = []
            skills_to_learn_raw = []
            context_user_skills = {
                'skills_known': [],
                'skills_to_learn': []
            }
            initial_data['skills_known'] = []
            initial_data['skills_to_learn'] = []

        form = CustomUserChangeForm(instance=request.user, initial=initial_data)

    context = {
        'form': form,
        'skill_choices': SKILL_CHOICES,
        'skill_colors': json.dumps(SKILL_COLORS),
        'context_user_skills': context_user_skills  # Add this to context
    }

    return render(request, 'users/profile_edit.html', context)
