from django import template
import json
import logging
import random
from users.skills_constants import get_skill_icon, get_skill_display, get_skill_color, SKILL_COLORS

register = template.Library()
logger = logging.getLogger(__name__)

# Random fallback colors for skills that don't have defined colors
FALLBACK_COLORS = [
    '#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
    '#1abc9c', '#d35400', '#34495e', '#16a085', '#c0392b',
    '#8e44ad', '#27ae60', '#f1c40f', '#e67e22', '#2980b9'
]

@register.filter
def get_item(dictionary, key):
    """Gets an item from a dictionary."""
    return dictionary.get(key)

@register.filter
def parse_json(json_string):
    """Parse a JSON string to a Python object."""
    if not json_string:
        return []

    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        logger.error(f"Error parsing JSON: {json_string}")
        return []

@register.filter
def skill_icon(skill):
    """Returns the Font Awesome icon class for a skill code."""
    return get_skill_icon(skill)

@register.filter
def skill_color(skill):
    """Returns the brand color for a skill code."""
    from users.skills_constants import SKILL_COLORS

    # Default color if no match is found
    default_color = '#6c757d'  # Bootstrap's secondary gray color

    if not skill:
        return default_color

    # Try uppercase (most common format in SKILL_COLORS dictionary)
    if isinstance(skill, str):
        color = SKILL_COLORS.get(skill.upper())
        if color:
            return color

    # Try as-is
    color = SKILL_COLORS.get(skill)
    if color:
        return color

    # Fallback to default
    return default_color

@register.filter
def skill_display(skill):
    """Returns the display name for a skill code."""
    return get_skill_display(skill)
