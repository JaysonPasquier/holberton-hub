from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def md(text):
    if text:
        return mark_safe(markdown.markdown(
            text,
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br'
            ]
        ))
    return ''
