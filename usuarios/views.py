from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioForm, AlunoForm, EmpresaForm
from .models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# =====================================================
# LOGOUT
# =====================================================
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("index")

# =====================================================
# CADASTRO DE USUÁRIO (Aluno, Empresa, Coordenação)
# =====================================================
def cadastro(request):
    if request.method == "POST":
        form_usuario = UsuarioForm(request.POST)
        form_aluno = AlunoForm(request.POST, request.FILES)
        form_empresa = EmpresaForm(request.POST)

        if form_usuario.is_valid():
            usuario = form_usuario.save(commit=False)
            usuario.is_active = True
            usuario.is_approved = False
            usuario.save()

            if usuario.tipo == "aluno" and form_aluno.is_valid():
                aluno = form_aluno.save(commit=False)
                aluno.usuario = usuario
                aluno.save()

            elif usuario.tipo == "empresa" and form_empresa.is_valid():
                empresa = form_empresa.save(commit=False)
                empresa.usuario = usuario
                empresa.save()

            messages.success(request, "Cadastro realizado! Aguarde aprovação da coordenação.")
            return redirect("login")

        else:
            messages.error(request, "Erro ao enviar o formulário. Verifique os campos e tente novamente.")
    else:
        form_usuario = UsuarioForm()
        form_aluno = AlunoForm()
        form_empresa = EmpresaForm()

    return render(request, "registration/cadastro.html", {
        "form_usuario": form_usuario,
        "form_aluno": form_aluno,
        "form_empresa": form_empresa,
    })
