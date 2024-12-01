class LangueParDefautMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Définir la langue par défaut si non définie
        if 'langue' not in request.session:
            request.session['langue'] = 'fr'
        response = self.get_response(request)
        return response
