
def theme_context(request):
    """Add theme information to the template context."""
    current_theme = request.session.get('theme', 'default')
    return {
        'current_theme': current_theme,
        'is_holberton_theme': current_theme == 'holberton',
    }
