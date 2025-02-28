from django import template
from projects.models import Project

register = template.Library()

@register.filter
def get_tech_display(tech_code):
    """Convertit le code technique en nom d'affichage"""
    tech_dict = dict(Project.TECH_CHOICES)
    return tech_dict.get(tech_code, tech_code)
