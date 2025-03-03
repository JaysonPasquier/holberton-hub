import logging
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.db.models import Q

from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm
from skills.models import Skill
from users.skills_constants import SKILL_CHOICES
from skills.categories import get_skills_by_category

logger = logging.getLogger(__name__)

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
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

        # Job type filter
        job_type = self.request.GET.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)

        # Status filter
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        # Skills filter
        skill = self.request.GET.get('skill')
        if skill:
            queryset = queryset.filter(skills__code=skill)

        # Location filter
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Company filter
        company = self.request.GET.get('company')
        if company:
            queryset = queryset.filter(company__icontains=company)

        # Employer filter
        employer = self.request.GET.get('employer')
        if employer:
            queryset = queryset.filter(employer__username__icontains=employer)

        # Salary range filters
        salary_min = self.request.GET.get('salary_min')
        if salary_min:
            try:
                queryset = queryset.filter(salary_min__gte=int(salary_min))
            except ValueError:
                pass

        salary_max = self.request.GET.get('salary_max')
        if salary_max:
            try:
                queryset = queryset.filter(salary_max__lte=int(salary_max))
            except ValueError:
                pass

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

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()

        if self.request.user.is_authenticated:
            # Check if user has already applied
            context['has_applied'] = JobApplication.objects.filter(
                job=job, applicant=self.request.user
            ).exists()
            context['is_owner'] = job.employer == self.request.user
            context['can_apply'] = not context['has_applied'] and not context['is_owner']

        # Add applications if user is the job creator
        if self.request.user.is_authenticated and job.employer == self.request.user:
            context['applications'] = job.applications.all()

        return context

@login_required
def job_create(request):
    """Create a new job posting."""
    if request.method == 'POST':
        logger.info(f"Received POST request to create job: {request.POST}")
        form = JobForm(request.POST)
        if form.is_valid():
            logger.info("Form is valid, creating job")
            job = form.save(commit=False)
            job.employer = request.user
            job.save()

            # Process selected skills
            selected_skills = request.POST.getlist('skills')
            logger.info(f"Selected skills: {selected_skills}")
            for skill_code in selected_skills:
                try:
                    # First try by code
                    skill = Skill.objects.get(code=skill_code)
                    job.skills.add(skill)
                    logger.info(f"Added skill {skill.name} to job by code")
                except Skill.DoesNotExist:
                    try:
                        # Try by name
                        skill = Skill.objects.get(name=skill_code)
                        job.skills.add(skill)
                        logger.info(f"Added skill {skill.name} to job by name")
                    except Skill.DoesNotExist:
                        # If the skill doesn't exist yet, create it
                        for code, name in SKILL_CHOICES:
                            if code == skill_code:
                                new_skill = Skill.objects.create(
                                    name=name,
                                    code=code,
                                    slug=slugify(name)
                                )
                                job.skills.add(new_skill)
                                logger.info(f"Created and added new skill: {new_skill.name}")
                                break
                        else:
                            # If not found in SKILL_CHOICES, create a generic one
                            new_skill = Skill.objects.create(
                                name=skill_code,
                                code=skill_code.upper().replace(' ', '_'),
                                slug=slugify(skill_code)
                            )
                            job.skills.add(new_skill)
                            logger.warning(f"Created generic skill: {new_skill.name}")

            messages.success(request, 'Your job has been posted!')

            # Redirection after creation
            try:
                try:
                    redirect_url = reverse('job_detail', kwargs={'pk': job.id})
                except:
                    redirect_url = reverse('job_detail', kwargs={'job_id': job.id})
                logger.info(f"Redirecting to: {redirect_url}")
                return redirect(redirect_url)
            except Exception as e:
                logger.error(f"Error creating redirect URL: {e}")
                messages.warning(request, "Job created, but there was an issue with redirection.")
                return redirect('job_list')
        else:
            logger.warning(f"Form validation errors: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()

    # Get all skills and organize them by category
    skills = Skill.objects.all()
    skills_by_category = get_skills_by_category()

    # Determine selected skills (for edit mode)
    selected_skills = []
    if hasattr(request, 'job'):
        selected_skills = [skill.code for skill in request.job.skills.all()]

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'selected_skills': selected_skills,
        'skill_choices': SKILL_CHOICES,
        'action': 'Create'
    })

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'

    def test_func(self):
        job = self.get_object()
        return job.employer == self.request.user

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

        messages.success(self.request, 'Job has been updated successfully.')
        return response

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        job = self.get_object()
        return job.employer == self.request.user

@login_required
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Check if the user has already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=job.pk)

    # Check if user is the job creator
    if job.employer == request.user:
        messages.warning(request, 'You cannot apply to your own job posting.')
        return redirect('job_detail', pk=job.pk)

    # Check if job is still open
    if not job.is_active:
        messages.warning(request, 'This job is no longer accepting applications.')
        return redirect('job_detail', pk=job.pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Your application has been submitted.')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobApplicationForm()

    return render(request, 'jobs/job_apply.html', {'form': form, 'job': job})

@login_required
def manage_application(request, application_id, action):
    application = get_object_or_404(JobApplication, id=application_id)
    job = application.job

    # Ensure only job creator can manage applications
    if request.user != job.employer:
        messages.error(request, "You don't have permission to manage this application.")
        return redirect('job_detail', pk=job.pk)

    if action == 'accept':
        application.status = 'accepted'
        messages.success(request, f"You've accepted {application.applicant.username}'s application.")
    elif action == 'reject':
        application.status = 'rejected'
        messages.success(request, f"You've rejected {application.applicant.username}'s application.")

    application.save()
    return redirect('job_detail', pk=job.pk)
