from django import forms
from .models import Job, JobApplication

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'deadline', 'max_participants', 'status']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'skills_required': forms.Textarea(attrs={'rows': 3}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Explain why you are interested in this job and why you would be a good fit.'
            }),
        }
