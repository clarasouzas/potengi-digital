from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [

    # ======================================
    # REDIRECIONAMENTO APÓS LOGIN
    # ======================================
    path("", views.redirecionar_dashboard, name="inicio"),

    # ======================================
    # ALUNO
    # ======================================
    path("aluno/", views.aluno_painel, name="aluno_painel"),
    path("aluno/vagas/", views.aluno_vagas, name="aluno_vagas"),
    path("aluno/candidaturas/", views.aluno_candidaturas, name="aluno_candidaturas"),

    # ======================================
    # EMPRESA
    # ======================================
    path("empresa/", views.empresa_painel, name="empresa_painel"),
    path("empresa/vagas/", views.empresa_vagas, name="empresa_vagas"),
    path("empresa/vagas/cadastrar/", views.empresa_cadastrar_vaga, name="empresa_cadastrar_vaga"),
    path("empresa/candidaturas/", views.empresa_candidaturas, name="empresa_candidaturas"),

    # ======================================
    # COORDENAÇÃO
    # ======================================
    path("coordenacao/", views.coordenacao_painel, name="coordenacao_painel"),
    path("coordenacao/aprovar-alunos/", views.aprovar_alunos, name="aprovar_alunos"),
    path("coordenacao/aprovar-empresas/", views.aprovar_empresas, name="aprovar_empresas"),
    path("coordenacao/aprovar-vagas/", views.aprovar_vagas, name="aprovar_vagas"),
    path("coordenacao/usuarios/", views.usuarios, name="usuarios"),
    path("coordenacao/relatorios/", views.relatorios, name="relatorios"),

    # ======================================
    # EDITAR PERFIL
    # ======================================
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
]
