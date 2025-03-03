from django import template
from users.skills_constants import get_skill_icon, get_skill_color, get_skill_display

register = template.Library()

@register.filter
def user_skill_icon(skill_code):
    """Return the Font Awesome icon class for a skill"""
    return get_skill_icon(skill_code)

@register.filter
def user_skill_color(skill_code):
    """Return the brand color for a skill"""
    return get_skill_color(skill_code)

@register.filter
def user_skill_display(skill_code):
    """Return the display name for a skill"""
    return get_skill_display(skill_code)
