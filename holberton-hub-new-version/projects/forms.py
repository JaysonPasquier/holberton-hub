from django import forms
from .models import Project, ProjectApplication

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'requirements', 'is_company_project',
            'is_paid', 'company', 'github_url', 'image', 'figma_url', 'other_url'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'is_company_project': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_company_project'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders and Bootstrap classes
        self.fields['title'].widget.attrs.update({'placeholder': 'E.g., "Social Media Dashboard"'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Describe your project'})
        self.fields['requirements'].widget.attrs.update({'placeholder': 'List any specific requirements (optional)'})
        self.fields['github_url'].widget.attrs.update({'placeholder': 'GitHub repository URL (optional)'})
        self.fields['figma_url'].widget.attrs.update({'placeholder': 'Figma design URL (optional)'})
        self.fields['other_url'].widget.attrs.update({'placeholder': 'Any other relevant URL (optional)'})
        self.fields['company'].widget.attrs.update({'placeholder': 'Company name (if applicable)'})

        # Make sure required fields are properly marked
        for field_name in ['title', 'description']:
            self.fields[field_name].required = True

class ProjectApplicationForm(forms.ModelForm):
    class Meta:
        model = ProjectApplication
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Explain why you want to join this project and what skills you can contribute...'}),
        }
