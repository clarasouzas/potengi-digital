from django.contrib import admin
from .models import Empresa, Aluno, Coordenador
from .models import Notificacao
admin.site.register(Empresa)
admin.site.register(Aluno)
admin.site.register(Coordenador)
admin.site.register(Notificacao)
