from django.urls import path
from . import views

urlpatterns = [
    # ==========================
    # PÁGINA INICIAL
    # ==========================
    path("", views.index, name="index"),

    # ==========================
    # VAGAS
    # ==========================
    path("vagas/", views.listar_vagas, name="listar_vagas"),
    #path("vagas/<int:vaga_id>/", views.detalhar_vaga, name="detalhar_vaga"),
    path("vagas/<int:vaga_id>/aprovar/", views.aprovar_vaga, name="aprovar_vaga"),

    # ==========================
    # CANDIDATURAS
    # ==========================
    path("vagas/<int:vaga_id>/candidatar/", views.candidatar_vaga, name="candidatar_vaga"),
    path(
        "candidaturas/<int:candidatura_id>/<str:status>/",
        views.atualizar_status_candidatura,
        name="atualizar_status_candidatura",
    ),
    path("perfis/<int:perfil_id>/", views.perfil_detalhe, name="perfil_detalhe"),
    path("perfis/", views.perfil_cursos, name="perfil_cursos"),
    # ==========================
    # NOTIFICAÇÕES E MENSAGENS
    # ==========================
    path("notificacoes/", views.notificacoes, name="notificacoes"),
    path("mensagens/", views.mensagens, name="mensagens"),

    # ==========================
    # CADASTRAR VAGgAS
    # ==========================
    path("vagas/cadastrar/", views.criar_vaga, name="criar_vaga"),
    path("vagas/minhas/", views.listar_vagas_empresa, name="listar_vagas_empresa"),
    path("vagas/editar/<int:id>/", views.editar_vaga, name="editar_vaga"),
    path("vagas/excluir/<int:id>/", views.excluir_vaga, name="excluir_vaga"),


    path('estudantes/', views.para_estudantes, name='para_estudantes'),
    path('empresas/', views.para_empresas, name='para_empresas'),
]