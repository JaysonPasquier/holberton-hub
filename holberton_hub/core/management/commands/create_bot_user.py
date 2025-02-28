from django.core.management.base import BaseCommand
from users.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates the HolbieBot user account'

    def handle(self, *args, **kwargs):
        try:
            bot_user = User.objects.create(
                username='HolbieBot',
                email='holbiebot@holberton.com',
                first_name='Holbie',
                last_name='Bot',
                is_active=True,
                is_bot=True  # Assurez-vous d'avoir ce champ dans votre modèle User
            )
            bot_user.set_password('HolbieBotSecurePassword123!')  # Changez ce mot de passe en production
            bot_user.save()

            self.stdout.write(self.style.SUCCESS('Bot user created successfully'))

        except IntegrityError:
            self.stdout.write(self.style.WARNING('Bot user already exists'))
