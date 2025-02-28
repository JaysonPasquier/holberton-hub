from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    technologies = forms.MultipleChoiceField(
        choices=Project.TECH_CHOICES,
        required=False,  # Rend le champ non obligatoire dans le formulaire
        widget=forms.CheckboxSelectMultiple(),
        help_text="Sélectionnez les technologies (optionnel)"
    )
    max_participants = forms.IntegerField(
        min_value=1,
        max_value=4,
        label='Nombre de participants',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '4'
        }),
        help_text='Minimum 1, maximum 4 participants'
    )

    class Meta:
        model = Project
        fields = [
            'titre',
            'description',
            'type_projet',
            'technologies',
            'github_link',
            'est_remunere',
            'remuneration_par_personne',
            'max_participants'
        ]
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'type_projet': forms.Select(attrs={'class': 'form-control'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'est_remunere': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'titre': 'Titre du projet',
            'description': 'Description',
            'type_projet': 'Type de projet',
            'technologies': 'Technologies requises',
            'github_link': 'Lien GitHub (optionnel)',
            'est_remunere': 'Projet rémunéré',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['github_link'].required = False
        if self.instance.type_projet == 'DEMODAY':
            self.fields['max_participants'].initial = 4
            self.fields['max_participants'].widget.attrs['readonly'] = True

        if user and user.is_company:
            self.fields['est_remunere'].widget = forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'onchange': 'toggleRemunerationField(this)'}
            )
            self.fields['remuneration_par_personne'].widget = forms.NumberInput(
                attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}
            )
        else:
            self.fields['remuneration_par_personne'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        type_projet = cleaned_data.get('type_projet')

        if type_projet == 'DEMODAY':
            cleaned_data['max_participants'] = 4

        return cleaned_data

    def clean_max_participants(self):
        max_participants = self.cleaned_data.get('max_participants')
        type_projet = self.cleaned_data.get('type_projet')

        if type_projet == 'DEMODAY' and (max_participants < 1 or max_participants > 4):
            raise forms.ValidationError("Pour un projet Demo Day, le nombre de participants doit être entre 1 et 4.")

        return max_participants
