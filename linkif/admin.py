from django.contrib import admin
from .models import (
    AreaAtuacao,
    Vaga,
    Candidatura,
    Notificacao,
    Mensagem,
    SiteConfig,
    HomeContent,
    PerfilFormacao,
    Competencia,
    AreaAtuacaoPerfil,
    MensagemContato,
)
admin.site.register(Competencia)
admin.site.register(AreaAtuacaoPerfil)
admin.site.register(PerfilFormacao)
admin.site.register(AreaAtuacao)
admin.site.register(Vaga)
admin.site.register(Candidatura)
admin.site.register(Notificacao)
admin.site.register(Mensagem)
admin.site.register(SiteConfig)
admin.site.register(HomeContent)
admin.site.register(MensagemContato)

