from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "usuarios"

urlpatterns = [
    # CADASTROS
    path("cadastro/", views.cadastro, name="cadastro"),
    path("cadastro/aluno/", views.cadastro_aluno, name="cadastro_aluno"),
    path("cadastro/empresa/", views.cadastro_empresa, name="cadastro_empresa"),
    path("cadastro/coord/", views.cadastro_coord, name="cadastro_coord"),
   
    # LOGIN
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"
    ),

    # LOGOUT
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

   
]
