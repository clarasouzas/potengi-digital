from django.urls import path
from . import views

app_name = "linkif"

urlpatterns = [

    # ============================
    # HOME
    # ============================
    path("", views.index, name="index"),

    # ============================
    # PÁGINAS PÚBLICAS
    # ============================
    path("para-estudantes/", views.para_estudantes, name="para_estudantes"),
    path("para-empresas/", views.para_empresas, name="para_empresas"),

    # ============================
    # PERFIS DE FORMAÇÃO
    # ============================
    path("perfis/", views.perfil_cursos, name="perfil_cursos"),
    path("perfis/<int:perfil_id>/", views.perfil_detalhe, name="perfil_detalhe"),

    # ============================
    # VAGAS PÚBLICAS (listagem)
    # ============================
    path("vagas/", views.listar_vagas, name="listar_vagas"),
    path("vagas/<int:vaga_id>/", views.vaga_detalhe, name="vaga_detalhe"),


    # candidatura (somente aluno)
    path("vagas/<int:vaga_id>/candidatar/", views.candidatar_vaga, name="candidatar_vaga"),

    # ============================
    # EXPLORAR ALUNOS (coordenação e empresas)
    # ============================
    path("explorar/", views.explorar_perfis, name="explorar"),



]
