from django.contrib.auth.models import AnonymousUser
from .models import User

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(id=user_id).first()
            if user:
                request.user = user
            else:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
        return self.get_response(request)
