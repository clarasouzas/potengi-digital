from django.urls import path
from . import views

app_name = "linkif"

urlpatterns = [

    # Início
    path("", views.index, name="index"),

    # Páginas públicas
    path("para-estudantes/", views.para_estudantes, name="para_estudantes"),
    path("para-empresas/", views.para_empresas, name="para_empresas"),

    # Perfis de Formação
    path("perfis/", views.perfil_cursos, name="perfil_cursos"),
    path("perfis/<int:perfil_id>/", views.perfil_detalhe, name="perfil_detalhe"),

    # Vagas Públicas (listagem)
    path("vagas/<int:vaga_id>/", views.vaga_detalhe, name="vaga_detalhe"),


    # candidatura (somente aluno)
    path("vagas/<int:vaga_id>/candidatar/", views.candidatar_vaga, name="candidatar_vaga"),

    # Vizualizar Alunos (coordenação e empresas)
    path("explorar/", views.explorar_perfis, name="explorar"),
    path("alunos/<int:pk>/", views.ver_perfil_aluno, name="ver_perfil_aluno"),

]
