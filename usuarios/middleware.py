from django.shortcuts import redirect
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount

class SocialLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and not request.user.is_anonymous:
            if not request.session.get('social_login_processed'):
                social_account = SocialAccount.objects.filter(user=request.user).first()
                
                if social_account and social_account.provider == 'google':
                    request.session['social_login_processed'] = True
                    
                    current_path = request.path
                    if 'cadastro/completar' not in current_path:
                        return redirect('usuarios:completar_cadastro')
        
        return response