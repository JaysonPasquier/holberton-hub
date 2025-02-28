from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User
import re  # Ajout de l'import manquant

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez le mot de passe'
        })
    )

    # Ajout des champs entreprise
    is_company = forms.BooleanField(required=False)
    company_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Site web de l\'entreprise'
        })
    )
    company_bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Description de l\'entreprise'
        })
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'is_company',
            'company_website',
            'company_bio',
            'linkedin_profile',  # Ajouter ces champs
            'github_profile'     # à la liste des fields
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Cette adresse email est déjà utilisée.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Les mots de passe ne correspondent pas.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        # Définir les attributs d'entreprise
        user.is_company = self.cleaned_data.get('is_company', False)
        if user.is_company:
            user.company_website = self.cleaned_data.get('company_website', '')
            user.company_bio = self.cleaned_data.get('company_bio', '')
            # Ajouter ces deux lignes pour sauvegarder les liens LinkedIn et GitHub
            user.linkedin_profile = self.cleaned_data.get('linkedin_profile', '')
            user.github_profile = self.cleaned_data.get('github_profile', '')
        else:
            user.company_website = ''
            user.company_bio = ''
            user.linkedin_profile = ''
            user.github_profile = ''

        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'profile_picture',
            'specialty', 'cohort', 'campus', 'bio',
            'github_profile', 'gitlab_profile',
            'linkedin_profile', 'portfolio_url',
            'medium_profile', 'dev_to_profile',
            'company_location', 'company_coordinates',
            'company_bio',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajout des placeholders pour tous les liens sociaux
        social_links = {
            'github_profile': 'https://github.com/votre-nom',
            'linkedin_profile': 'https://www.linkedin.com/in/votre-nom',
        }

        for field, placeholder in social_links.items():
            if field in self.fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': placeholder
                })

        if not self.instance.is_company:
            # Si ce n'est pas une entreprise, on utilise les champs existants
            self.fields = {
                'username': forms.CharField(
                    label="Nom d'utilisateur",
                    widget=forms.TextInput(attrs={'class': 'form-control'})
                ),
                'email': forms.EmailField(
                    widget=forms.EmailInput(attrs={'class': 'form-control'})
                ),
                'specialty': forms.ChoiceField(
                    choices=User.SPECIALTIES,
                    widget=forms.Select(attrs={'class': 'form-control'})
                ),
                'cohort': forms.ChoiceField(
                    choices=User.COHORT_CHOICES,
                    required=False,
                    widget=forms.Select(attrs={
                        'class': 'form-control',
                        'placeholder': 'Sélectionnez votre cohorte'
                    })
                ),
                'campus': forms.ChoiceField(
                    choices=User.CAMPUS_CHOICES,
                    required=False,
                    widget=forms.Select(attrs={'class': 'form-control'})
                ),
                'bio': forms.CharField(
                    required=False,
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
                ),
                'github_profile': forms.URLField(
                    required=False,
                    widget=forms.URLInput(attrs={'class': 'form-control'})
                ),
                'linkedin_profile': forms.URLField(
                    required=False,
                    widget=forms.URLInput(attrs={'class': 'form-control'})
                ),
                'profile_picture': forms.ImageField(
                    required=False,
                    widget=forms.FileInput(attrs={'class': 'form-control'})
                ),
                'skills': forms.MultipleChoiceField(
                    choices=User.TECH_CHOICES,
                    required=False,
                    widget=forms.CheckboxSelectMultiple(attrs={'class': 'skill-checkbox'})
                )
            }
        else:
            # Configuration uniquement pour les entreprises
            self.fields['username'].label = "Nom de l'entreprise"
            self.fields['company_location'] = forms.CharField(
                label="Localisation (ville)",
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
            self.fields['company_coordinates'] = forms.CharField(
                label="Coordonnées GPS (optionnel)",
                required=False,
                help_text="Format: latitude,longitude (ex: 48.8566,2.3522)",
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
            self.fields['company_bio'] = forms.CharField(
                label="Présentation de l'entreprise",
                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
            )
            # Garder uniquement les champs nécessaires pour les entreprises
            keep_fields = [
                'username', 'email', 'company_location', 'company_coordinates',
                'company_bio', 'github_profile', 'linkedin_profile', 'profile_picture'
            ]
            for field_name in list(self.fields.keys()):
                if field_name not in keep_fields:
                    del self.fields[field_name]

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.is_company:
            # Validation des coordonnées GPS si fournies
            coordinates = cleaned_data.get('company_coordinates')
            if coordinates:
                if not re.match(r'^-?\d+\.?\d*,-?\d+\.?\d*$', coordinates):
                    raise forms.ValidationError({
                        'company_coordinates': "Format des coordonnées GPS invalide. Utilisez: latitude,longitude"
                    })
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Sauvegarder les compétences
        if 'skills' in self.cleaned_data:
            user.skills = self.cleaned_data['skills']

        if 'profile_picture' in self.files:
            user.profile_picture = self.files['profile_picture']

        if commit:
            user.save()
        return user
