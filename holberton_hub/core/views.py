from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_navbar'] = False  # Pour afficher la navbar sur la landing page
        return context
