from django.core.management.base import BaseCommand
from skills.models import Skill
from users.skills_constants import SKILL_CHOICES

class Command(BaseCommand):
    help = 'Populate code field for existing skills'

    def handle(self, *args, **options):
        skills = Skill.objects.all()
        updated = 0

        # Dictionary mapping skill names to their codes
        name_to_code = {name.lower(): code for code, name in SKILL_CHOICES}

        for skill in skills:
            skill_name_lower = skill.name.lower()

            # If skill doesn't have a code yet
            if not skill.code or skill.code == 'CODE':
                # Look for a match in SKILL_CHOICES
                if skill_name_lower in name_to_code:
                    skill.code = name_to_code[skill_name_lower]
                    skill.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated {skill.name} with code {skill.code}"))
                    updated += 1
                else:
                    # Create a code from the name
                    skill.code = skill.name.upper().replace(' ', '_')
                    skill.save()
                    self.stdout.write(self.style.WARNING(f"Generated code {skill.code} for {skill.name}"))
                    updated += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully updated {updated} skills"))
