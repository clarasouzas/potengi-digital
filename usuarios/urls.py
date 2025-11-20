from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailAuthenticationForm
from .views import excluir_perfil

app_name = 'usuarios'

urlpatterns = [
    # =============================
    # CADASTRO PERSONALIZADO
    # =============================
    path("cadastro/", views.cadastro, name="cadastro"),
    path('cadastro/aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/empresa/', views.cadastro_empresa, name='cadastro_empresa'),
    path('cadastro/coord/', views.cadastro_coord, name='cadastro_coord'),
    path("perfil/<int:id>/", views.perfil_aluno, name="perfil_aluno"),
   

    # =============================
    # AUTENTICAÇÃO PADRÃO DJANGO
    # =============================
path(
    "login/",
    auth_views.LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=EmailAuthenticationForm
    ),
    name="login"
),    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html"), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name="password_change_done"),

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),

]





