from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a pinned guide project'

    def handle(self, *args, **kwargs):
        try:
            admin = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found'))
            return

        guide_project = Project.objects.create(
            title="📚 Guide - Comment utiliser Holberton Hub",
            description="""
### Bienvenue sur Holberton Hub! 🚀

Ce projet sert de guide pour comprendre le fonctionnement de la plateforme.

#### 🎯 Fonctionnalités principales:

1. **Création de projets**
   - Cliquez sur "Créer un projet"
   - Remplissez les informations requises
   - Choisissez le type de projet et les technologies
   - Définissez la taille d'équipe souhaitée

2. **Rejoindre des projets**
   - Parcourez les projets disponibles
   - Filtrez par type ou technologie
   - Postulez via le bouton "Rejoindre"
   - Attendez la réponse du créateur

3. **Communication**
   - Chat en temps réel dans chaque projet
   - Liste des membres connectés
   - Commandes bot (/help, /project, etc.)
   - Notifications pour les candidatures

4. **Profil utilisateur**
   - Photo de profil personnalisable
   - Liens GitHub et LinkedIn
   - Liste des projets créés/rejoints
   - Statut en ligne/hors ligne

#### 💡 Conseils:
- Complétez bien votre profil
- Décrivez clairement vos projets
- Soyez actif dans les discussions
- Collaborez avec respect

#### 🤝 Besoin d'aide?
Utilisez le chatbot pour plus d'informations ou contactez un administrateur.

*Ce projet est épinglé pour servir de référence permanente.*
            """,
            creator=admin,
            project_type='FUND',  # ou autre type approprié
            is_pinned=True,
            status='INFO'  # Ajoutez ce statut dans les choix du modèle
        )

        self.stdout.write(self.style.SUCCESS('Guide project created successfully'))
