from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from .skills_constants import SKILL_CHOICES, get_skill_icon, get_skill_color

class SkillsSelectWidget(forms.Widget):
    template_name = 'users/widgets/skills_select.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.choices = SKILL_CHOICES

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context['widget']['choices'] = self.choices
        context['widget']['value'] = value or []
        context['widget']['icons'] = {choice[0]: get_skill_icon(choice[0]) for choice in self.choices}
        context['widget']['colors'] = {choice[0]: get_skill_color(choice[0]) for choice in self.choices}

        return mark_safe(render_to_string(self.template_name, context))
