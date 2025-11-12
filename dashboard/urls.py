from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dashboard_index"),
    path("aluno/", views.dashboard_aluno, name="dashboard_aluno"),
    path("empresa/", views.dashboard_empresa, name="dashboard_empresa"),
    path("coordenacao/", views.dashboard_coordenacao, name="dashboard_coordenacao"),
]