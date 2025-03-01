from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import cloudinary
import json

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .cloudinary_init import initialize_cloudinary
from .skills_constants import SKILL_CHOICES

# Ensure Cloudinary is initialized
initialize_cloudinary()

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

        # Set the skills on the user model
        user = form.save(commit=False)
        user.skills_known = json.dumps(skills_known)
        user.skills_to_learn = json.dumps(skills_to_learn)
        return super().form_valid(form)
