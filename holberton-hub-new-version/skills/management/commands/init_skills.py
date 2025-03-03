from django.core.management.base import BaseCommand
from django.utils.text import slugify
from skills.models import Skill
from users.skills_constants import SKILL_CHOICES

class Command(BaseCommand):
    help = 'Initialize skills from the SKILL_CHOICES constant'

    def handle(self, *args, **options):
        count = 0

        for code, name in SKILL_CHOICES:
            skill, created = Skill.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'slug': slugify(name)
                }
            )

            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Created skill: {name}'))
            else:
                self.stdout.write(f'Skill already exists: {name}')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} skills'))
