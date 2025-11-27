from django.apps import AppConfig

class ConfigConfig(AppConfig):
    '''
    PATCH para ignorar validadores de username no allauth
    '''
    name = 'config'
    
    def ready(self):
        import allauth.account.adapter
        from allauth.account import app_settings as account_settings
        
        original_clean_username = allauth.account.adapter.DefaultAccountAdapter.clean_username
        
        def patched_clean_username(self, username):
            if username is None:
                return ""
            return original_clean_username(self, username)
        
        allauth.account.adapter.DefaultAccountAdapter.clean_username = patched_clean_username
        
        def get_patched_username_validators():
            return []
        
        account_settings.USERNAME_VALIDATORS = get_patched_username_validators