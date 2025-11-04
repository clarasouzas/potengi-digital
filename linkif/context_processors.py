from .models import SiteConfig, HomeContent

def site_context(request):
    """
    Adiciona configurações globais e conteúdo da home
    a todos os templates do site.
    """
    site_config = SiteConfig.objects.first()
    home_content = HomeContent.objects.first()

    return {
        "site_config": site_config,
        "home_content": home_content,
    }
