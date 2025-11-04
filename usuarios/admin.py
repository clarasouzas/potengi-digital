from django.contrib import admin
from .models import Usuario, Aluno, Empresa, Coordenador


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("email", "tipo", "is_approved", "is_staff")
    list_filter = ("tipo", "is_approved", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "curso")
    search_fields = ("usuario__email", "curso")


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome_fantasia", "cnpj", "area_atuacao", "usuario")
    search_fields = ("nome_fantasia", "cnpj")


@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ("usuario", "setor")
