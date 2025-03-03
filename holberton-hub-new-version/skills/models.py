from django.db import models
from django.utils.text import slugify
from users.skills_constants import SKILL_CHOICES, get_skill_display

class Skill(models.Model):
    """Model representing a skill (programming language, technology, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=False, null=False, unique=True, default='CODE')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        # Ensure code is uppercase
        if self.code:
            self.code = self.code.upper()
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        """Get the display name from the constants if available"""
        if self.code:
            return get_skill_display(self.code)
        return self.name
