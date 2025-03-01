from django import template
from users.skills_constants import get_skill_icon, get_skill_display, get_skill_color

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Gets an item from a dictionary."""
    return dictionary.get(key)

@register.filter
def skill_icon(skill):
    """Returns the Font Awesome icon class for a skill code."""
    return get_skill_icon(skill)

@register.filter
def skill_color(skill):
    """Returns the brand color for a skill code."""
    return get_skill_color(skill)

@register.filter
def skill_display(skill):
    """Returns the display name for a skill code."""
    return get_skill_display(skill)
