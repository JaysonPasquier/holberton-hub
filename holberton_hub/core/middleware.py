from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = [
            '/',  # Autoriser la page d'accueil
            reverse('login'),
            reverse('register'),
            '/static/',
            '/admin/',
        ]

        if not request.user.is_authenticated:
            current_path = request.path
            if not any(current_path.startswith(path) for path in public_paths):
                return redirect('login')
        return self.get_response(request)
