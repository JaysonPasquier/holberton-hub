from django.shortcuts import render, redirect, get_object_or_404
from django.db import models  # Ajout de cet import
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Candidature
from .serializers import ProjectSerializer, CandidatureSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from django.utils import timezone
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
import logging

logger = logging.getLogger(__name__)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        project = self.get_object()
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project, applicant=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrer par type de projet
        type_projet = self.request.GET.get('type_projet')
        if type_projet:
            queryset = queryset.filter(type_projet=type_projet)

        # Filtrer les projets d'entreprise
        est_projet_entreprise = self.request.GET.get('est_projet_entreprise')
        if est_projet_entreprise:
            queryset = queryset.filter(est_projet_entreprise=est_projet_entreprise.lower() == 'true')

        # Filtrer par technologie
        technologie = self.request.GET.get('technologie')
        if technologie:
            # Filtrer en utilisant une approche compatible avec SQLite
            queryset = queryset.filter(technologies__icontains=f'"{technologie}"')

        # Tri
        sort = self.request.GET.get('sort', 'recent')
        if sort == 'most_likes':
            queryset = queryset.annotate(like_count=models.Count('likes')).order_by('-like_count')
        elif sort == 'least_likes':
            queryset = queryset.annotate(like_count=models.Count('likes')).order_by('like_count')
        elif sort == 'most_upvotes':
            queryset = queryset.annotate(
                vote_score=models.Count('upvotes') - models.Count('downvotes')
            ).order_by('-vote_score')
        elif sort == 'least_upvotes':
            queryset = queryset.annotate(
                vote_score=models.Count('upvotes') - models.Count('downvotes')
            ).order_by('vote_score')
        elif sort == 'oldest':
            queryset = queryset.order_by('date_creation')
        elif sort == 'most_participants':
            queryset = queryset.annotate(num_participants=models.Count('participants')).order_by('-num_participants')
        elif sort == 'least_participants':
            queryset = queryset.annotate(num_participants=models.Count('participants')).order_by('num_participants')
        else:  # recent (default)
            queryset = queryset.order_by('-date_creation')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_types'] = Project.TYPE_CHOICES
        context['tech_choices'] = Project.TECH_CHOICES
        if self.request.user.is_authenticated:
            context['archived_projects'] = Project.objects.filter(est_archive=True)
        context['pinned_projects'] = Project.objects.filter(est_epingle=True)
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.createur = self.request.user  # Définir le créateur comme l'utilisateur actuel
        response = super().form_valid(form)
        return response

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_edit.html'
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.createur != request.user:
            return redirect('project_detail', pk=project.pk)
        return super().dispatch(request, *args, **kwargs)

@login_required
def project_apply(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        if request.user == project.createur:  # Utiliser createur au lieu de creator
            messages.error(request, "Vous ne pouvez pas postuler à votre propre projet!")
            return redirect('project_detail', pk=pk)

        message = request.POST.get('message')
        if message:
            # Vérifier si une candidature existe déjà
            existing_application = Candidature.objects.filter(
                projet=project,
                candidat=request.user
            ).exists()

            if existing_application:
                messages.warning(request, "Vous avez déjà postulé à ce projet!")
            else:
                Candidature.objects.create(
                    projet=project,
                    candidat=request.user,
                    message=message
                )
                messages.success(request, "Votre candidature a été envoyée avec succès!")
        else:
            messages.error(request, "Le message de candidature est requis!")
    return redirect('project_detail', pk=pk)

def application_status(request, pk):
    candidature = get_object_or_404(Candidature, pk=pk)
    if request.user == candidature.projet.createur and request.method == 'POST':
        status = request.POST.get('status')
        if status in ['ACCEPTE', 'REFUSE']:
            candidature.statut = status
            candidature.save()
            if status == 'ACCEPTE':
                candidature.projet.participants.add(candidature.candidat)
            messages.success(request, f'Candidature {status.lower()}')
    return redirect('project_detail', pk=candidature.projet.pk)

@login_required
def archive_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user == project.creator and request.method == 'POST':
        project.est_archive = True
        project.archived_date = timezone.now()
        project.status = 'ARCHIVED'
        project.save()
        messages.success(request, "Le projet a été archivé avec succès.")
    return redirect('project_detail', pk=pk)

@login_required
@require_POST
def like_project(request, pk):
    try:
        project = get_object_or_404(Project, pk=pk)
        logger.debug(f"Like request received for project {pk} from user {request.user}")

        if request.user in project.likes.all():
            project.likes.remove(request.user)
            liked = False
        else:
            project.likes.add(request.user)
            liked = True

        response_data = {
            'liked': liked,
            'count': project.likes.count()
        }
        logger.debug(f"Sending response: {response_data}")
        return JsonResponse(response_data)
    except Exception as e:
        logger.error(f"Error in like_project: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def vote_project(request, pk):
    try:
        project = get_object_or_404(Project, pk=pk)
        data = json.loads(request.body) if request.body else {'vote_type': None}
        vote_type = data.get('vote_type')

        was_upvoted = request.user in project.upvotes.all()
        was_downvoted = request.user in project.downvotes.all()

        # Supprimer tous les votes existants
        project.upvotes.remove(request.user)
        project.downvotes.remove(request.user)

        # Appliquer le nouveau vote seulement si c'est différent du vote précédent
        message = "Vote retiré"
        if vote_type == 'up' and not was_upvoted:
            project.upvotes.add(request.user)
            message = "Vote positif enregistré"
        elif vote_type == 'down' and not was_downvoted:
            project.downvotes.add(request.user)
            message = "Vote négatif enregistré"

        return JsonResponse({
            'score': project.score,
            'message': message
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
