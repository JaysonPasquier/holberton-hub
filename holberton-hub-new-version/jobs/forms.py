from django import forms
from .models import Job, JobApplication

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company', 'location', 'job_type',
            'description', 'requirements', 'application_url',
            'salary_min', 'salary_max'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders and Bootstrap classes
        self.fields['title'].widget.attrs.update({'placeholder': 'E.g., "Full Stack Developer"'})
        self.fields['company'].widget.attrs.update({'placeholder': 'Company name'})
        self.fields['location'].widget.attrs.update({'placeholder': 'E.g., "San Francisco, CA" or "Remote"'})
        self.fields['application_url'].widget.attrs.update({'placeholder': 'URL for external application (optional)'})
        self.fields['salary_min'].widget.attrs.update({'placeholder': 'Min annual salary'})
        self.fields['salary_max'].widget.attrs.update({'placeholder': 'Max annual salary'})

        # Make sure required fields are properly marked
        for field_name in ['title', 'company', 'location', 'job_type', 'description']:
            self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')

        # If both salary fields are provided, ensure min <= max
        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                raise forms.ValidationError('Minimum salary cannot be greater than maximum salary.')

        return cleaned_data

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us why you\'re a good fit for this position...'}),
        }
