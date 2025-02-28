from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserUpdateForm, UserRegistrationForm  # Suppression de UserRegisterForm
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from projects.models import Project
from django.contrib.auth import login, authenticate
from django.urls import reverse

class UserRegisterView(CreateView):
    form_class = UserRegistrationForm  # Changé de UserRegisterForm à UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
        return response

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)

        if user.is_company:
            # Pour les profils entreprise
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.company_location = form.cleaned_data['company_location']
            user.company_coordinates = form.cleaned_data['company_coordinates']
            user.github_profile = form.cleaned_data['github_profile']
            user.linkedin_profile = form.cleaned_data['linkedin_profile']
            user.company_bio = form.cleaned_data['company_bio']
        else:
            # Pour les profils étudiants, ajouter la sauvegarde des compétences
            if 'skills' in form.cleaned_data:
                user.skills = form.cleaned_data['skills']

        if 'profile_picture' in self.request.FILES:
            user.profile_picture = self.request.FILES['profile_picture']

        # S'assurer que les compétences sont préservées
        if 'skills' in form.cleaned_data:
            user.skills = form.cleaned_data['skills']

        user.save()
        messages.success(self.request, 'Profil mis à jour avec succès!')
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        # Ajouter les compétences actuelles aux données initiales
        if self.request.user.skills:
            initial['skills'] = self.request.user.skills
        return initial

@login_required
def profile_view(request):
    context = {
        'user': request.user,
        'projects_created': Project.objects.filter(createur=request.user, est_archive=False),
        'projects_joined': Project.objects.filter(participants=request.user, est_archive=False),
        'projects_archived': Project.objects.filter(createur=request.user, est_archive=True),
    }
    return render(request, 'users/profile.html', context)

def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    context = {
        'user': profile_user,  # Important : utiliser 'user' comme clé pour la cohérence des templates
        'projects_created': Project.objects.filter(createur=profile_user, est_archive=False),
        'projects_joined': Project.objects.filter(participants=profile_user, est_archive=False),
        'is_own_profile': request.user == profile_user
    }
    return render(request, 'users/profile.html', context)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def online(self, request):
        """API endpoint pour obtenir la liste des utilisateurs et leur statut"""
        users = User.objects.all().order_by('-last_activity')
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                # Vérifier si le nom d'utilisateur existe déjà
                if User.objects.filter(username=user.username).exists():
                    messages.error(request, "Ce nom d'utilisateur est déjà pris.")
                    return render(request, 'users/register.html', {'form': form})

                # Vérifier si l'email existe déjà
                if User.objects.filter(email=user.email).exists():
                    messages.error(request, "Cette adresse email est déjà utilisée.")
                    return render(request, 'users/register.html', {'form': form})

                user.save()
                messages.success(request, 'Inscription réussie! Vous pouvez maintenant vous connecter.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Une erreur s'est produite lors de l'inscription : {str(e)}")
        else:
            # Afficher les erreurs spécifiques du formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    if field == 'username':
                        messages.error(request, f"Nom d'utilisateur : {error}")
                    elif field == 'email':
                        messages.error(request, f"Email : {error}")
                    else:
                        messages.error(request, error)
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {
        'form': form,
        'hide_navbar': True
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if not remember_me:
                # Si "Se souvenir de moi" n'est pas coché, définir la session pour expirer à la fermeture du navigateur
                request.session.set_expiry(0)
            else:
                # Si "Se souvenir de moi" est coché, définir la session pour durer 2 semaines
                request.session.set_expiry(1209600)  # 2 semaines en secondes

            return redirect('landing')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'users/login.html')
