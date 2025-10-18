from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index.html"),
    path('', views.login, name="login.html"),
    path('', views.cadastro_candidato, name="cadastro_candidato.html"),
    path('', views.cadastro_empresa, name="cadastro_empresa.html"),
    path('', views.vagas, name="vagas.html"),
    path('', views.perfil_cursos, name="perfil_cursos.html"),
    
]
