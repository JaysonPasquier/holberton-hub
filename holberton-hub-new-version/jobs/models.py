from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Job(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='jobs_created')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    skills_required = models.TextField(blank=True, help_text="Comma separated list of required skills")
    deadline = models.DateField(blank=True, null=True)
    max_participants = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job_detail', args=[str(self.id)])

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='job_applications')
    message = models.TextField()
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')

    class Meta:
        unique_together = ['job', 'applicant']

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
