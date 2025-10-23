from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('vagas/', views.vagas, name="vagas"),
    path('perfil_cursos/', views.perfil_cursos, name="perfil_cursos"),
     path('vagas/', views.vagas, name='vagas'),
    path('detalhar/', views.detalhar, name='detalhar'),

    
]
