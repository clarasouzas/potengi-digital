from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [

    # Início (pós-login)
    path("", views.inicio, name="inicio"),


    # Aluno
    path("aluno/", views.aluno_painel, name="aluno_painel"),
    path("aluno/candidaturas/", views.aluno_candidaturas, name="aluno_candidaturas"),
    path(
        "aluno/candidatura/<int:cand_id>/cancelar/",
        views.cancelar_candidatura,
        name="cancelar_candidatura"
    ),
    path("aluno/mensagens/", views.aluno_mensagens, name="aluno_mensagens"),
    path("aluno/mensagens/enviar/", views.enviar_mensagem, name="enviar_mensagem"),


    # Empresa
    path("empresa/", views.empresa_painel, name="empresa_painel"),

    path("empresa/mensagens/", views.empresa_mensagens, name="empresa_mensagens"),
    path("empresa/mensagens/enviar/", views.enviar_mensagem, name="enviar_mensagem"),
    
    # Vagas
    path("empresa/vagas/", views.empresa_vagas, name="empresa_vagas"),
    path("empresa/vagas/cadastrar/", views.empresa_cadastrar_vaga, name="empresa_cadastrar_vaga"),
    path("empresa/vagas/editar/<int:vaga_id>/", views.empresa_editar_vaga, name="empresa_editar_vaga"),
    path("empresa/vagas/excluir/<int:vaga_id>/", views.empresa_excluir_vaga, name="empresa_excluir_vaga"),

    # Candidaturas
    path("empresa/candidaturas/", views.empresa_candidaturas, name="empresa_candidaturas"),
    path(
        "empresa/candidatura/<int:cand_id>/",
        views.empresa_candidatura_detalhe,
        name="empresa_candidatura_detalhe"
    ),

    # Perfis públicos
    path("alunos/<int:pk>/", views.ver_perfil_aluno, name="ver_perfil_aluno"),
    path("empresas/<int:pk>/", views.ver_perfil_empresa, name="ver_perfil_empresa"),


    # Coordenação - Painel
    path("coordenacao/", views.coordenacao_painel, name="coordenacao_painel"),


    # Coordenação - Aprovações
    path("coordenacao/aprovar_alunos/", views.aprovar_alunos, name="aprovar_alunos"),
    path("coordenacao/aprovar_empresas/", views.aprovar_empresas, name="aprovar_empresas"),
    path("coordenacao/aprovar_vagas/", views.aprovar_vagas, name="aprovar_vagas"),

    # Ações
    path(
        "coordenacao/aprovar-empresa/<int:user_id>/",
        views.aprovar_empresa_action,
        name="aprovar_empresa_action"
    ),
    path(
        "coordenacao/aprovar-aluno/<int:user_id>/",
        views.aprovar_aluno_action,
        name="aprovar_aluno_action"
    ),
    path(
        "coordenacao/reprovar-empresa/<int:user_id>/",
        views.reprovar_empresa_action,
        name="reprovar_empresa_action"
    ),
    path(
        "coordenacao/reprovar-aluno/<int:user_id>/",
        views.reprovar_aluno_action,
        name="reprovar_aluno_action"
    ),

    # Aprovar / reprovar vagas
    path(
        "coordenacao/vagas/<int:vaga_id>/aprovar/",
        views.aprovar_vaga_action,
        name="aprovar_vaga_action"
    ),
    path(
        "coordenacao/vagas/<int:vaga_id>/reprovar/",
        views.reprovar_vaga_action,
        name="reprovar_vaga_action"
    ),


    # Coordenação - Gerenciar Usuários
    path("coordenacao/usuarios/", views.coordenacao_usuarios, name="usuarios"),
    path(
        "coordenacao/usuarios/<int:user_id>/editar/",
        views.coordenacao_usuario_editar,
        name="usuario_editar"
    ),
    path(
        "coordenacao/usuarios/<int:user_id>/excluir/",
        views.coordenacao_usuario_excluir,
        name="usuario_excluir"
    ),
    path(
        "coordenacao/usuarios/<int:user_id>/tornar-admin/",
        views.tornar_admin,
        name="tornar_admin"
    ),


    # Coordenação - Gerenciar Empresas 
    path("coordenacao/empresas/", views.coordenacao_empresas, name="empresas"),
    path(
        "coordenacao/empresas/<int:empresa_id>/editar/",
        views.coordenacao_empresa_editar,
        name="empresa_editar"
    ),
    path(
        "coordenacao/empresas/<int:empresa_id>/excluir/",
        views.coordenacao_empresa_excluir,
        name="empresa_excluir"
    ),


    # Coordenação — Perfis de Formação
    path("coordenacao/perfis/", views.listar_perfis, name="listar_perfis"),
    path("coordenacao/perfis/novo/", views.editar_perfil_formacao, name="novo_perfil_formacao"),
    path(
        "coordenacao/perfis/editar/<int:pk>/",
        views.editar_perfil_formacao,
        name="editar_perfil_formacao"
    ),
    path(
        "coordenacao/perfis/excluir/<int:pk>/",
        views.excluir_perfil_formacao,
        name="excluir_perfil_formacao"
    ),

    # Competências
    path(
        "coordenacao/perfis/<int:perfil_id>/competencia/adicionar/",
        views.adicionar_competencia,
        name="adicionar_competencia"
    ),
    path(
        "coordenacao/perfis/competencia/remover/<int:pk>/",
        views.remover_competencia,
        name="remover_competencia"
    ),

    # Áreas
    path(
        "coordenacao/perfis/<int:perfil_id>/area/adicionar/",
        views.adicionar_area,
        name="adicionar_area"
    ),
    path(
        "coordenacao/perfis/area/remover/<int:pk>/",
        views.remover_area,
        name="remover_area"
    ),


    # Configurações do Site
    path("configuracoes/site/", views.site_config, name="site_config"),


    # Perfil do Proprio usuário
    path("perfil/", views.meu_perfil, name="perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),


    # Relatórios
    path("coordenacao/relatorios/", views.relatorios, name="relatorios"),
    
    #Mensagens
    path("coordenacao/mensagens/", views.mensagens_contato, name="mensagens_contato"),
    path("mensagens/<int:pk>/responder/", views.responder_mensagem, name="responder_mensagem"),

]
