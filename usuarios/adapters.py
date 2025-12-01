from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
import requests

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def _is_suap_email(self, email):
        """
        Verifica se o email é de domínio do SUAP/IFRN
        """
        suap_domains = [
            'academico.ifrn.edu.br',
            'escolar.ifrn.edu.br', 
            'ifrn.edu.br',
        ]
        
        if not email or '@' not in email:
            return False
            
        domain = email.split('@')[1].lower()
        return domain in suap_domains
    
    def pre_social_login(self, request, sociallogin):
        """
        Executado ANTES do login social
        Aqui podemos capturar o tipo da sessão
        """
        tipo_sessao = request.session.get('social_login_type')
        if tipo_sessao:
            sociallogin.state['user_type'] = tipo_sessao
            
    def populate_user(self, request, sociallogin, data):
        """
        Popula o usuário com dados do provedor social
        """
        user = super().populate_user(request, sociallogin, data)
        
        provider = sociallogin.account.provider
        email = data.get('email', '')
        
        if provider == 'suap':
            user.tipo = 'aluno'
            user.is_approved = True
            
            extra_data = sociallogin.account.extra_data
            user.nome = extra_data.get('nome_usual', '').strip()
            user.curso = ''
            
        elif provider == 'google':
            tipo_from_state = sociallogin.state.get('user_type')
            
            if tipo_from_state:
                user.tipo = tipo_from_state
                
                if tipo_from_state == 'aluno':
                    user.is_approved = self._is_suap_email(email)
                else:
                    user.is_approved = False
                    
            else:
                tipo_sessao = request.session.get('social_login_type')
                if tipo_sessao:
                    user.tipo = tipo_sessao
                    if tipo_sessao == 'aluno':
                        user.is_approved = self._is_suap_email(email)
                    else:
                        user.is_approved = False
                else:
                    if self._is_suap_email(email):
                        user.tipo = 'aluno'
                        user.is_approved = True
                    else:
                        user.tipo = ''
                        user.is_approved = False
                        request.session['social_login_needs_type'] = True
            
            extra_data = sociallogin.account.extra_data
            display_name = extra_data.get('name', '') or data.get('name', '')
            if not user.nome and display_name:
                user.nome = display_name.strip()
            
            user.curso = ''
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        
        user.save()
                
        if sociallogin.account.provider == 'google':
            self._download_google_photo(user, sociallogin)
        elif sociallogin.account.provider == 'suap':
            self._download_suap_photo(user, sociallogin)
            self._buscar_curso(user, sociallogin)
        
        return user
    
    def get_connect_redirect_url(self, request, socialaccount):
        """
        Redireciona após login social
        """
        from django.urls import reverse
        
        user = socialaccount.user
        
        if 'social_login_type' in request.session:
            del request.session['social_login_type']
        
        if request.session.get('social_login_needs_type'):
            del request.session['social_login_needs_type']
            return reverse('usuarios:escolher_tipo')
        
        if not user.tipo:
            return reverse('usuarios:escolher_tipo')
        
        if user.tipo == 'empresa' and not user.is_approved:
            return reverse('usuarios:aguardando_aprovacao')
        
        if user.tipo == 'aluno' and not user.is_approved:
            return reverse('usuarios:aguardando_aprovacao_aluno')
        
        return reverse('linkif:index')
        
    def _download_google_photo(self, user, sociallogin):
        try:
            extra_data = sociallogin.account.extra_data
            foto_url = extra_data.get('picture')
            
            if foto_url:
                if '=' in foto_url:
                    base_url = foto_url.split('=')[0]
                    foto_url = f"{base_url}=s200-c"
                
                response = requests.get(foto_url, timeout=10)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        extension = 'jpg'
                    elif 'png' in content_type:
                        extension = 'png'
                    else:
                        extension = 'jpg'
                    
                    filename = f"google_photo_{user.id}.{extension}"
                    user.foto.save(filename, ContentFile(response.content), save=True)
                
        except Exception as e:
            print(f"Erro ao baixar foto do Google: {e}")
    
    def _download_suap_photo(self, user, sociallogin):
        try:
            extra_data = sociallogin.account.extra_data
            foto_url = extra_data.get('url_foto_150x200') or extra_data.get('foto')
            
            if foto_url:
                response = requests.get(foto_url, timeout=10)
                if response.status_code == 200:
                    filename = f"suap_photo_{user.id}.jpg"
                    user.foto.save(filename, ContentFile(response.content), save=True)
                
        except Exception as e:
            print(f"Erro ao baixar foto: {e}")
    
    def _buscar_curso(self, user, sociallogin):
        curso = self._get_curso_from_meus_dados(sociallogin)
        if curso:
            user.curso = curso
            user.save()
    
    def _get_curso_from_meus_dados(self, sociallogin):
        try:
            access_token = sociallogin.token.token
            headers = {'Authorization': f'Bearer {access_token}'}
            endpoint = 'https://suap.ifrn.edu.br/api/rh/meus-dados/'
            
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                dados = response.json()
                return self._find_curso_in_dados(dados)
            
        except Exception as e:
            print(f"Erro ao buscar curso: {e}")
        
        return ""
    
    def _find_curso_in_dados(self, dados):
        caminhos = [
            dados.get('vinculo', {}).get('curso'),
        ]
        
        for caminho in caminhos:
            if caminho and str(caminho).strip():
                return str(caminho).strip()
        
        return ""
