from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from skills.models import Skill

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    is_company_project = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False, blank=True)  # Only relevant for company projects
    company = models.CharField(max_length=100, blank=True, null=True)  # Only filled if is_company_project is True

    # Links
    github_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    figma_url = models.URLField(blank=True, null=True)
    other_url = models.URLField(blank=True, null=True)

    # Relationships
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')
    skills = models.ManyToManyField(Skill, blank=True, related_name='projects')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

class ProjectApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_applications')
    message = models.TextField()
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')

    class Meta:
        unique_together = ['project', 'applicant']

    def __str__(self):
        return f"{self.applicant.username} - {self.project.title}"
