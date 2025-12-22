from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [

    # Início (pós-login)
    path("", views.inicio, name="inicio"),

    # ---------------------------
    #         ALUNO
    # ---------------------------
    path("aluno/", views.aluno_painel, name="aluno_painel"),
    path("aluno/candidaturas/", views.aluno_candidaturas, name="aluno_candidaturas"),
    path(
        "aluno/candidatura/<int:cand_id>/cancelar/",
        views.cancelar_candidatura,
        name="cancelar_candidatura"
    ),

    # ---------------------------
    #         ALUNO
    # ---------------------------
    path('aluno/mensagens/', views.aluno_mensagens, name='aluno_mensagens'),
    path('aluno/mensagens/enviar', views.aluno_enviar_mensagem, name='aluno_enviar_mensagem'),

    # ---------------------------
    #         EMPRESA
    # ---------------------------
    path("empresa/", views.empresa_painel, name="empresa_painel"),
    path("empresa/mensagens/", views.empresa_mensagens, name="empresa_mensagens"),
    path("empresa/mensagens/enviar/", views.empresa_enviar_mensagem, name='empresa_enviar_mensagem'),

    # VAGAS DA EMPRESA
    path("empresa/vagas/", views.empresa_vagas, name="empresa_vagas"),
    path("empresa/vagas/cadastrar/", views.empresa_cadastrar_vaga, name="empresa_cadastrar_vaga"),
    path("empresa/vagas/editar/<int:vaga_id>/", views.empresa_editar_vaga, name="empresa_editar_vaga"),
    path("empresa/vagas/excluir/<int:vaga_id>/", views.empresa_excluir_vaga, name="empresa_excluir_vaga"),

    # Acompanhar vagas da própria empresa
    path("empresa/acompanhar_vagas/", views.empresa_acompanhar_vagas, name="empresa_acompanhar_vagas"),
    path(
        "empresa/vagas/etapa/<int:vaga_id>/",
        views.empresa_atualizar_etapa,
        name="empresa_atualizar_etapa"
    ),

    # CANDIDATURAS EM VAGAS DA EMPRESA
    path("empresa/candidaturas/", views.empresa_candidaturas, name="empresa_candidaturas"),
    path(
        "empresa/candidatura/<int:cand_id>/",
        views.empresa_candidatura_detalhe,
        name="empresa_candidatura_detalhe"
    ),

    # ---------------------------
    #       PERFIS PÚBLICOS
    # ---------------------------
    path("alunos/<int:pk>/", views.ver_perfil_aluno, name="ver_perfil_aluno"),
    path("empresas/<int:pk>/", views.ver_perfil_empresa, name="ver_perfil_empresa"),

    # Coordenação também atualiza etapas
    path("vaga/<int:vaga_id>/etapa/", views.atualizar_etapa_vaga, name="atualizar_etapa_vaga"),

    # ---------------------------
    #         COORDENAÇÃO
    # ---------------------------
    path("coordenacao/", views.coordenacao_painel, name="coordenacao_painel"),

    # Gerenciar alunos/empresas → TABELA ÚNICA
    path("coordenacao/gerenciar/<str:tipo>/", views.gerenciar_por_tipo, name="gerenciar_por_tipo"),
    path("coordenacao/usuario/status/", views.usuario_mudar_status, name="usuario_mudar_status"),
    path("coordenacao/usuario/<int:pk>/excluir/", views.usuario_excluir, name="usuario_excluir"),
    path("coordenacao/usuario/<int:pk>/editar/", views.usuario_editar, name="usuario_editar"),

    

    path("coordenacao/aprovar-aluno/<int:user_id>/", views.aprovar_aluno_action, name="aprovar_aluno_action"),
    path("coordenacao/reprovar-aluno/<int:user_id>/", views.reprovar_aluno_action, name="reprovar_aluno_action"),

    path("coordenacao/aprovar-empresa/<int:user_id>/", views.aprovar_empresa_action, name="aprovar_empresa_action"),
    path("coordenacao/reprovar-empresa/<int:user_id>/", views.reprovar_empresa_action, name="reprovar_empresa_action"),

    # ---------------------------
    #         VAGAS
    # ---------------------------
    path("coordenacao/aprovar_vagas/", views.aprovar_vagas, name="aprovar_vagas"),
    path("coordenacao/vagas/<int:vaga_id>/aprovar/", views.aprovar_vaga_action, name="aprovar_vaga_action"),
    path("coordenacao/vagas/<int:vaga_id>/reprovar/", views.reprovar_vaga_action, name="reprovar_vaga_action"),

    path("coordenacao/vagas/", views.acompanhar_vagas, name="acompanhar_vagas"),
    path("coordenacao/vagas/etapa/<int:vaga_id>/", views.atualizar_etapa_vaga, name="atualizar_etapa_vaga"),
    # Minhas vagas da coordenação
    path("coordenacao/minhas-vagas/", 
        views.coordenacao_minhas_vagas, 
        name="coordenacao_minhas_vagas"),
    path("coordenacao/cadastrar_vaga/",
     views.coordenacao_cadastrar_vaga,
     name="coordenacao_cadastrar_vaga"),
    path("coordenacao/editar-vaga/<int:vaga_id>/",
     views.coordenacao_editar_vaga,
     name="coordenacao_editar_vaga"),

path("coordenacao/excluir-vaga/<int:vaga_id>/",
     views.coordenacao_excluir_vaga,
     name="coordenacao_excluir_vaga"),


    # ---------------------------
    #     PERFIS DE FORMAÇÃO
    # ---------------------------
    path("coordenacao/perfis/", views.listar_perfis, name="listar_perfis"),
    path("coordenacao/perfis/novo/", views.editar_perfil_formacao, name="novo_perfil_formacao"),
    path("coordenacao/perfis/editar/<int:pk>/", views.editar_perfil_formacao, name="editar_perfil_formacao"),
    path("coordenacao/perfis/excluir/<int:pk>/", views.excluir_perfil_formacao, name="excluir_perfil_formacao"),

    path("coordenacao/perfis/<int:perfil_id>/competencia/adicionar/", views.adicionar_competencia, name="adicionar_competencia"),
    path("coordenacao/perfis/competencia/remover/<int:pk>/", views.remover_competencia, name="remover_competencia"),

    path("coordenacao/perfis/<int:perfil_id>/area/adicionar/", views.adicionar_area, name="adicionar_area"),
    path("coordenacao/perfis/area/remover/<int:pk>/", views.remover_area, name="remover_area"),

    # ---------------------------
    #     CONFIG DO SITE
    # ---------------------------
    path("configuracoes/site/", views.site_config, name="site_config"),

    # ---------------------------
    #     PERFIL DO USUÁRIO
    # ---------------------------
    path("perfil/", views.meu_perfil, name="perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),

    # ---------------------------
    #       RELATÓRIOS
    # ---------------------------
    path("coordenacao/relatorios/", views.relatorios, name="relatorios"),

    # ---------------------------
    #       MENSAGENS
    # ---------------------------
    path("coordenacao/mensagens/", views.mensagens_contato, name="mensagens_contato"),
    path("mensagens/<int:pk>/responder/", views.responder_mensagem, name="responder_mensagem"),
]
