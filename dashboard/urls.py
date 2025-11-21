from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [

    # ======================================
    # PÓS-LOGIN
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

    path("coordenacao/aprovar_alunos/", views.aprovar_alunos, name="aprovar_alunos"),
    path("coordenacao/aprovar_empresas/", views.aprovar_empresas, name="aprovar_empresas"),
    path("coordenacao/aprovar_vagas/", views.aprovar_vagas, name="aprovar_vagas"),

    # Gerenciar usuários
    path("coordenacao/usuarios/", views.usuarios, name="usuarios"),
    path("coordenacao/usuarios/<int:user_id>/editar/", views.coordenacao_usuario_editar, name="usuario_editar"),
    path("coordenacao/usuarios/<int:user_id>/excluir/", views.coordenacao_usuario_excluir, name="usuario_excluir"),

    # Gerenciar empresas
    path("coordenacao/empresas/", views.coordenacao_empresas, name="empresas"),
    path("coordenacao/empresas/<int:empresa_id>/editar/", views.coordenacao_empresa_editar, name="empresa_editar"),
    path("coordenacao/empresas/<int:empresa_id>/excluir/", views.coordenacao_empresa_excluir, name="empresa_excluir"),

    # Perfil
    path("perfil/", views.meu_perfil, name="perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),

    path("coordenacao/relatorios/", views.relatorios, name="relatorios"),

]
