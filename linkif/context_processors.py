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
def splash_screen_processor(request):
    show_splash = False
    if request.user.is_authenticated:
        if not request.session.get("splash_seen", False):
            show_splash = True
            request.session["splash_seen"] = True
    return {"show_splash": show_splash}