from django import template
from users.skills_constants import get_skill_icon as get_icon, get_skill_color as get_color

register = template.Library()

@register.filter
def get_skill_icon(skill_code):
    """Get the Font Awesome icon class for a skill code"""
    if not skill_code:
        return 'fas fa-code'  # Default icon
    return get_icon(skill_code)

@register.filter
def get_skill_color(skill_code):
    """Get the brand color for a skill code"""
    if not skill_code:
        return '#6c757d'  # Default color - Bootstrap's secondary gray
    return get_color(skill_code)
