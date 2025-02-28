from django import template
from projects.models import Project

register = template.Library()

@register.filter
def get_tech_name(tech_code):
    """Convert tech code to display name"""
    tech_dict = dict(Project.TECH_CHOICES)
    return tech_dict.get(tech_code, tech_code)