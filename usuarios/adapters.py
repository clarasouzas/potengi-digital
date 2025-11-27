from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class SuapSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def populate_user(self, request, sociallogin, data):
        """
        Usa o populate_user padrão para adicionar campos extras
        """
        user = super().populate_user(request, sociallogin, data)
        
        user.tipo = 'aluno'
        user.is_approved = True
        
        if not user.nome:
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            user.nome = f"{first_name} {last_name}".strip()
        
        user.curso = data.get('vinculo', {}).get('curso', '')
        
        return user