from django.db import models
from users.models import User
from django.conf import settings

class Project(models.Model):
    TYPE_CHOICES = [
        ('CYBER', 'Cybersécurité'),
        ('WEB', 'Web Fullstack'),
        ('ARVR', 'AR/VR'),
        ('AI', 'Intelligence Artificielle'),
        ('BLOCKCHAIN', 'Blockchain'),
        ('DEMODAY', 'Demo Day'),
    ]

    TECH_CHOICES = [
        ('PYTHON', 'Python'),
        ('DJANGO', 'Django'),
        ('FLASK', 'Flask'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('JAVASCRIPT', 'JavaScript'),
        ('TYPESCRIPT', 'TypeScript'),
        ('REACT', 'React'),
        ('NEXTJS', 'Next.js'),
        ('VUEJS', 'Vue.js'),
        ('NUXTJS', 'Nuxt.js'),
        ('ANGULAR', 'Angular'),
        ('SVELTE', 'Svelte'),
        ('NODEJS', 'Node.js'),
        ('EXPRESS', 'Express.js'),
        ('PHP', 'PHP'),
        ('LARAVEL', 'Laravel'),
        ('SYMFONY', 'Symfony'),
        ('JAVA', 'Java'),
        ('SPRING', 'Spring'),
        ('KOTLIN', 'Kotlin'),
        ('SWIFT', 'Swift'),
        ('CSHARP', 'C#'),
        ('DOTNET', '.NET'),
        ('RUBY', 'Ruby'),
        ('RAILS', 'Ruby on Rails'),
        ('GO', 'Go'),
        ('RUST', 'Rust'),
        ('DOCKER', 'Docker'),
        ('KUBERNETES', 'Kubernetes'),
        ('GIT', 'Git'),
        ('GITHUB', 'GitHub'),
        ('GITLAB', 'GitLab'),
        ('BITBUCKET', 'Bitbucket'),
        ('AWS', 'AWS'),
        ('AZURE', 'Azure'),
        ('GCP', 'Google Cloud'),
        ('DIGITALOCEAN', 'DigitalOcean'),
        ('HEROKU', 'Heroku'),
        ('VERCEL', 'Vercel'),
        ('NETLIFY', 'Netlify'),
        ('NGINX', 'Nginx'),
        ('APACHE', 'Apache'),
        ('MYSQL', 'MySQL'),
        ('POSTGRESQL', 'PostgreSQL'),
        ('MONGODB', 'MongoDB'),
        ('REDIS', 'Redis'),
        ('ELASTICSEARCH', 'Elasticsearch'),
        ('GRAPHQL', 'GraphQL'),
        ('LINUX', 'Linux'),
        ('UBUNTU', 'Ubuntu'),
        ('WINDOWS', 'Windows'),
        ('MACOS', 'macOS'),
        ('ANDROID', 'Android'),
        ('IOS', 'iOS'),
        ('FLUTTER', 'Flutter'),
        ('REACT_NATIVE', 'React Native'),
        ('WORDPRESS', 'WordPress'),
        ('DRUPAL', 'Drupal'),
        ('BOOTSTRAP', 'Bootstrap'),
        ('TAILWIND', 'Tailwind CSS'),
        ('SASS', 'Sass'),
        ('WEBPACK', 'Webpack'),
        ('BABEL', 'Babel'),
        ('NPM', 'npm'),
        ('YARN', 'Yarn'),
        ('JENKINS', 'Jenkins'),
        ('TRAVIS', 'Travis CI'),
        ('CIRCLECI', 'CircleCI'),
        ('ANSIBLE', 'Ansible'),
        ('TERRAFORM', 'Terraform'),
        ('JIRA', 'Jira'),
        ('TRELLO', 'Trello'),
        ('FIGMA', 'Figma'),
        ('JEST', 'Jest'),
        ('CYPRESS', 'Cypress'),
        ('SELENIUM', 'Selenium'),
        ('PYTORCH', 'PyTorch'),
        ('TENSORFLOW', 'TensorFlow'),
    ]

    STATUT_CHOICES = [
        ('OUVERT', 'Ouvert'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_projet = models.CharField(max_length=20, choices=TYPE_CHOICES)
    statut_projet = models.CharField(max_length=20, choices=STATUT_CHOICES, default='OUVERT')
    est_remunere = models.BooleanField(default=False)
    remuneration_par_personne = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Montant de la rémunération par personne (en €)"
    )
    est_projet_entreprise = models.BooleanField(default=False)
    technologies = models.JSONField(
        default=list,
        null=True,  # Permettre les valeurs NULL
        blank=True,  # Permettre les champs vides
        help_text="Les technologies ne sont pas obligatoires"
    )
    github_link = models.URLField(blank=True, null=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projets_crees')
    participants = models.ManyToManyField(User, related_name='projets_participes', blank=True)
    max_participants = models.IntegerField(default=4)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_archive = models.BooleanField(default=False)
    date_archivage = models.DateTimeField(null=True, blank=True)
    est_epingle = models.BooleanField(default=False)
    description_courte = models.CharField(max_length=255, blank=True)  # Ajout du champ

    # Système de likes (simple)
    likes = models.ManyToManyField(
        User,
        related_name='liked_projects',
        blank=True
    )

    # Système d'upvotes/downvotes
    upvotes = models.ManyToManyField(
        User,
        related_name='upvoted_projects',
        blank=True
    )
    downvotes = models.ManyToManyField(
        User,
        related_name='downvoted_projects',
        blank=True
    )

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def score(self):
        return self.upvotes.count() - self.downvotes.count()

    @property
    def est_actif(self):
        return not self.est_archive

    def save(self, *args, **kwargs):
        # Assurez-vous que technologies est une liste vide si elle est None
        if self.technologies is None:
            self.technologies = []

        if self.createur.is_company:
            self.est_projet_entreprise = True
        # Générer la description courte à partir de la description complète
        if not self.description_courte and self.description:
            # Si la description fait plus de 200 caractères, la tronquer
            if len(self.description) > 200:
                self.description_courte = self.description[:200] + "..."
            else:
                self.description_courte = self.description
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_creation']
        # ordering = ['-est_epingle', '-date_creation']

    def __str__(self):
        return self.titre

class Candidature(models.Model):
    CHOIX_STATUT = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTE', 'Accepté'),
        ('REFUSE', 'Refusé')
    ]

    projet = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='candidatures')
    candidat = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    statut = models.CharField(max_length=10, choices=CHOIX_STATUT, default='EN_ATTENTE')
    date_creation = models.DateTimeField(auto_now_add=True)

    def get_statut_display(self):
        return dict(self.CHOIX_STATUT)[self.statut]

    class Meta:
        ordering = ['-date_creation']  # Plus récentes en premier
