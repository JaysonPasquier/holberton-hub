from django import template
from django.template.defaultfilters import stringfilter
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def markdown_to_html(text):
    """Convert markdown text to HTML"""
    return mark_safe(markdown.markdown(text))
