from django.contrib import admin
from .models import Project, Candidature

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titre', 'createur', 'type_projet', 'statut_projet', 'est_remunere', 'est_archive')
    list_filter = ('type_projet', 'statut_projet', 'est_remunere', 'est_archive')
    search_fields = ('titre', 'description', 'createur__username')
    date_hierarchy = 'date_creation'

@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('projet', 'candidat', 'statut', 'date_creation')
    list_filter = ('statut',)
    search_fields = ('projet__titre', 'candidat__username')
    date_hierarchy = 'date_creation'
