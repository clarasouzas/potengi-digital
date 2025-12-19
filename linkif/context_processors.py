from .models import SiteConfig

def site_context(request):
    """
    Adiciona configurações globais e conteúdo da home
    a todos os templates do site.
    """
    site_config = SiteConfig.objects.first()

    return {
        "site_config": site_config,
    }
