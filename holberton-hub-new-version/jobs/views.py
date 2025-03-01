from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    ordering = ['-created_at']
    paginate_by = 10

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
            context['is_owner'] = job.created_by == self.request.user
            context['can_apply'] = not context['has_applied'] and not context['is_owner']

        # Add applications if user is the job creator
        if self.request.user.is_authenticated and job.created_by == self.request.user:
            context['applications'] = job.applications.all()

        return context

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'

    def test_func(self):
        job = self.get_object()
        return job.created_by == self.request.user

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        job = self.get_object()
        return job.created_by == self.request.user

@login_required
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Check if the user has already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=job.pk)

    # Check if user is the job creator
    if job.created_by == request.user:
        messages.warning(request, 'You cannot apply to your own job posting.')
        return redirect('job_detail', pk=job.pk)

    # Check if job is still open
    if job.status != 'open':
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
    if request.user != job.created_by:
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
