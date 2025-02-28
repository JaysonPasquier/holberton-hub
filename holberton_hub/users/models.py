from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone

class User(AbstractUser):
    SPECIALTIES = [
        ('FOND', 'Fondamentaux'),
        ('CYBER', 'Cybersécurité'),
        ('AI', 'Intelligence Artificielle'),
        ('ARVR', 'AR/VR'),
        ('BLOCK', 'BlockChaine'),
        ('WEB', 'Web FullStack')
    ]

    CAMPUS_CHOICES = [
        ('PARIS', 'Paris'),
        ('BORDEAUX', 'Bordeaux'),
        ('CAUSSADE', 'Caussade'),
        ('DIJON', 'Dijon'),
        ('LAVAL', 'Laval'),
        ('LILLE', 'Lille'),
        ('RENNES', 'Rennes'),
        ('RODEZ', 'Rodez'),
        ('SENS', 'Sens'),
        ('THONON', 'Thonon-les-Bains'),
        ('TOULOUSE', 'Toulouse'),

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
        ('PHOTOSHOP', 'Photoshop'),
        ('ILLUSTRATOR', 'Illustrator'),
        ('JEST', 'Jest'),
        ('CYPRESS', 'Cypress'),
        ('SELENIUM', 'Selenium'),
        ('PYTORCH', 'PyTorch'),
        ('TENSORFLOW', 'TensorFlow'),
    ]

    COHORT_CHOICES = [
        ('C#22', 'Cohorte 22'),
        ('C#23', 'Cohorte 23'),
        ('C#24', 'Cohorte 24'),
        ('C#25', 'Cohorte 25'),
        ('C#26', 'Cohorte 26'),
    ]

    is_company = models.BooleanField(default=False)
    company_website = models.URLField(blank=True, null=True)
    company_bio = models.TextField(null=True, blank=True)  # Make this field optional
    username = models.CharField(
        max_length=30,  # Limite à 30 caractères
        unique=True,
        error_messages={
            'unique': "Ce nom d'utilisateur est déjà pris.",
            'max_length': "Le nom d'utilisateur ne peut pas dépasser 30 caractères."
        }
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Cette adresse email est déjà utilisée.'
        }
    )
    is_bot = models.BooleanField(default=False)
    specialty = models.CharField(max_length=5, choices=SPECIALTIES, blank=True)
    cohort = models.CharField(
        max_length=10,
        choices=COHORT_CHOICES,
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    github_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    campus = models.CharField(
        max_length=100,  # Augmenter la longueur max
        blank=True,      # Permettre les valeurs vides
        verbose_name='Campus',
        help_text='Entrez le nom de votre campus'
    )
    profile_picture = CloudinaryField(
        'image',
        folder='profile_pictures/',
        null=True,
        blank=True
    )
    company_location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ville ou adresse complète de l'entreprise"
    )
    company_coordinates = models.CharField(
        max_length=100,
        blank=True,
        help_text="Format: latitude,longitude (ex: 48.8566,2.3522)"
    )
    last_activity = models.DateTimeField(auto_now=True)
    skills = models.JSONField(default=list, blank=True)  # Stocke les compétences comme une liste

    # Ajout des nouveaux champs pour les liens sociaux
    portfolio_url = models.URLField(max_length=200, blank=True, null=True)
    gitlab_profile = models.URLField(max_length=200, blank=True, null=True)
    medium_profile = models.URLField(max_length=200, blank=True, null=True)
    dev_to_profile = models.URLField(max_length=200, blank=True, null=True)

    @property
    def is_online(self):
        if not self.last_activity:
            return False
        return (timezone.now() - self.last_activity).total_seconds() < 300  # 5 minutes

    class Meta:
        indexes = [
            models.Index(fields=['is_company']),
            models.Index(fields=['email']),
        ]
