import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Project, ProjectApplication
from .forms import ProjectForm, ProjectApplicationForm
from skills.models import Skill
from users.skills_constants import SKILL_CHOICES
from skills.categories import get_skills_by_category

logger = logging.getLogger(__name__)

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Basic search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(company__icontains=query)
            )

        # Project type filter
        project_type = self.request.GET.get('type')
        if project_type == 'personal':
            queryset = queryset.filter(is_company_project=False)
        elif project_type == 'company':
            queryset = queryset.filter(is_company_project=True)

        # Status filter
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'closed':
            queryset = queryset.filter(is_active=False)

        # Payment filter
        paid = self.request.GET.get('paid')
        if paid == 'paid':
            queryset = queryset.filter(is_paid=True)
        elif paid == 'unpaid':
            queryset = queryset.filter(is_paid=False)

        # Skills filter
        skill = self.request.GET.get('skill')
        if skill:
            queryset = queryset.filter(skills__code=skill)

        # Creator filter
        creator = self.request.GET.get('creator')
        if creator:
            queryset = queryset.filter(creator__username__icontains=creator)

        # Date range filters
        date_from = self.request.GET.get('date_from')
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                queryset = queryset.filter(created_at__gte=date_from)
            except ValueError:
                pass

        date_to = self.request.GET.get('date_to')
        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d')
                # Add one day to include the entire day
                date_to += timedelta(days=1)
                queryset = queryset.filter(created_at__lt=date_to)
            except ValueError:
                pass

        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add skill choices for the dropdown
        context['skill_choices'] = SKILL_CHOICES
        # Add categorized skills
        context['skills_by_category'] = get_skills_by_category()
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        if self.request.user.is_authenticated:
            # Check if user has already applied
            context['has_applied'] = ProjectApplication.objects.filter(
                project=project, applicant=self.request.user
            ).exists()
            context['is_owner'] = project.creator == self.request.user
            context['can_apply'] = not context['has_applied'] and not context['is_owner']

        # Add applications if user is the project creator
        if self.request.user.is_authenticated and project.creator == self.request.user:
            context['applications'] = project.applications.all()

        return context

@login_required
def project_create(request):
    """Create a new project."""
    if request.method == 'POST':
        logger.info(f"Received POST request to create project: {request.POST}")
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("Form is valid, creating project")
            project = form.save(commit=False)
            project.creator = request.user
            project.save()

            # Process selected skills
            selected_skills = request.POST.getlist('skills')
            logger.info(f"Selected skills: {selected_skills}")
            for skill_code in selected_skills:
                try:
                    # First try by code
                    skill = Skill.objects.get(code=skill_code)
                    project.skills.add(skill)
                    logger.info(f"Added skill {skill.name} to project by code")
                except Skill.DoesNotExist:
                    try:
                        # Try by name
                        skill = Skill.objects.get(name=skill_code)
                        project.skills.add(skill)
                        logger.info(f"Added skill {skill.name} to project by name")
                    except Skill.DoesNotExist:
                        # If the skill doesn't exist yet, create it
                        for code, name in SKILL_CHOICES:
                            if code == skill_code:
                                new_skill = Skill.objects.create(
                                    name=name,
                                    code=code,
                                    slug=slugify(name)
                                )
                                project.skills.add(new_skill)
                                logger.info(f"Created and added new skill: {new_skill.name}")
                                break
                        else:
                            # If not found in SKILL_CHOICES, create a generic one
                            new_skill = Skill.objects.create(
                                name=skill_code,
                                code=skill_code.upper().replace(' ', '_'),
                                slug=slugify(skill_code)
                            )
                            project.skills.add(new_skill)
                            logger.warning(f"Created generic skill: {new_skill.name}")

            messages.success(request, 'Your project has been created!')
            return redirect('project_detail', pk=project.pk)
        else:
            logger.warning(f"Form validation errors: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()

    # Get all skills and organize them by category
    skills = Skill.objects.all()
    skills_by_category = get_skills_by_category()

    # Determine selected skills (for edit mode)
    selected_skills = []
    if hasattr(request, 'project'):
        selected_skills = [skill.code for skill in request.project.skills.all()]

    return render(request, 'projects/project_form.html', {
        'form': form,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'selected_skills': selected_skills,
        'skill_choices': SKILL_CHOICES,
        'action': 'Create'
    })

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def test_func(self):
        project = self.get_object()
        return project.creator == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()
        context['skills_by_category'] = get_skills_by_category()
        context['selected_skills'] = [skill.code for skill in self.object.skills.all()]
        context['skill_choices'] = SKILL_CHOICES
        context['action'] = 'Update'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        # Handle skills update
        self.object.skills.clear()
        selected_skills = self.request.POST.getlist('skills')

        for skill_code in selected_skills:
            try:
                skill = Skill.objects.get(code=skill_code)
            except Skill.DoesNotExist:
                for code, name in SKILL_CHOICES:
                    if code == skill_code:
                        skill = Skill.objects.create(
                            name=name,
                            code=code,
                            slug=slugify(name)
                        )
                        break
                else:
                    skill = Skill.objects.create(
                        name=skill_code,
                        code=skill_code.upper().replace(' ', '_'),
                        slug=slugify(skill_code)
                    )
            self.object.skills.add(skill)

        messages.success(self.request, 'Project has been updated successfully.')
        return response

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        project = self.get_object()
        return project.creator == self.request.user

@login_required
def apply_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Check if the user has already applied
    if ProjectApplication.objects.filter(project=project, applicant=request.user).exists():
        messages.warning(request, 'You have already applied to this project.')
        return redirect('project_detail', pk=project.pk)

    # Check if user is the project creator
    if project.creator == request.user:
        messages.warning(request, 'You cannot apply to your own project.')
        return redirect('project_detail', pk=project.pk)

    # Check if project is still active
    if not project.is_active:
        messages.warning(request, 'This project is no longer accepting applications.')
        return redirect('project_detail', pk=project.pk)

    if request.method == 'POST':
        form = ProjectApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.project = project
            application.applicant = request.user
            application.save()
            messages.success(request, 'Your application has been submitted.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectApplicationForm()

    return render(request, 'projects/project_apply.html', {'form': form, 'project': project})

@login_required
def manage_project_application(request, application_id, action):
    application = get_object_or_404(ProjectApplication, id=application_id)
    project = application.project

    # Ensure only project creator can manage applications
    if request.user != project.creator:
        messages.error(request, "You don't have permission to manage this application.")
        return redirect('project_detail', pk=project.pk)

    if action == 'accept':
        application.status = 'accepted'
        messages.success(request, f"You've accepted {application.applicant.username}'s application.")
    elif action == 'reject':
        application.status = 'rejected'
        messages.success(request, f"You've rejected {application.applicant.username}'s application.")

    application.save()
    return redirect('project_detail', pk=project.pk)
