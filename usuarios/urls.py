from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    cadastro,
    cadastro_aluno,
    cadastro_empresa,
)

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", cadastro, name="cadastro"),

    path("cadastro/aluno/", cadastro_aluno, name="cadastro_aluno"),
    path("cadastro/empresa/", cadastro_empresa, name="cadastro_empresa"),

    # login/logout do Django
    path("login/",
         auth_views.LoginView.as_view(template_name="registration/login.html"),
         name="login"),
    path("logout/",
         auth_views.LogoutView.as_view(),
         name="logout"),

]
