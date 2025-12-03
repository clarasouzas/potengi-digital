from django.contrib import admin
from .models import (
    Vaga,
    Candidatura,
    SiteConfig,
    PerfilFormacao,
    Competencia,
    AreaAtuacaoPerfil,
    MensagemContato,
)
admin.site.register(Competencia)
admin.site.register(AreaAtuacaoPerfil)
admin.site.register(PerfilFormacao)
admin.site.register(Vaga)
admin.site.register(Candidatura)
admin.site.register(SiteConfig)
admin.site.register(MensagemContato)

