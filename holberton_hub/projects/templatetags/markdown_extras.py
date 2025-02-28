from django import template
from django.template.defaultfilters import stringfilter
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def convert_markdown(value):
    return mark_safe(markdown.markdown(value, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.tables']))
