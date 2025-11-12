from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import AlunoForm, EmpresaForm, CoordenacaoForm
from .models import Usuario, Aluno, Empresa, Coordenador


# =====================================================
# LOGOUT
# =====================================================
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("usuarios:login")


# =====================================================
# CADASTRO GERAL (com abas)
# =====================================================
def cadastro(request):
    """Renderiza o formulário de cadastro com abas dinâmicas"""
    forms = [
        ("aluno", AlunoForm(), "usuarios:cadastro_aluno", "primary", "bi-mortarboard-fill", "Cadastro de Aluno"),
        ("empresa", EmpresaForm(), "usuarios:cadastro_empresa", "success", "bi-building-fill", "Cadastro de Empresa"),
        ("coord", CoordenacaoForm(), "usuarios:cadastro_coord", "secondary", "bi-person-gear", "Cadastro de Coordenação"),
    ]
    return render(request, "registration/cadastro.html", {"forms": forms})


# =====================================================
# CADASTRO DE ALUNO
# =====================================================
def cadastro_aluno(request):
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            senha = form.cleaned_data.get("senha")
            confirmar_senha = form.cleaned_data.get("confirmar_senha")

            if senha != confirmar_senha:
                messages.error(request, "As senhas não coincidem.")
                return redirect("usuarios:cadastro")

            usuario = Usuario.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=senha,
                tipo="aluno",
            )

            Aluno.objects.create(
                usuario=usuario,
                curso=form.cleaned_data["curso"],
            )

            messages.success(request, "Aluno cadastrado com sucesso!")
            return redirect("usuarios:login")

        messages.error(request, "Verifique os campos e tente novamente.")
    return redirect("usuarios:cadastro")


# =====================================================
# CADASTRO DE EMPRESA
# =====================================================
def cadastro_empresa(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            senha = form.cleaned_data.get("senha")
            confirmar_senha = form.cleaned_data.get("confirmar_senha")

            if senha != confirmar_senha:
                messages.error(request, "As senhas não coincidem.")
                return redirect("usuarios:cadastro")

            # cria o usuário base
            usuario = Usuario.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=senha,
                tipo="empresa",
            )

            # cria perfil da empresa
            Empresa.objects.create(
                nome_empresa=form.cleaned_data["nome_empresa"],
                razao_social=form.cleaned_data["razao_social"],
                cnpj=form.cleaned_data["cnpj"],
                telefone=form.cleaned_data["telefone"],
                email=form.cleaned_data["email"],
                site=form.cleaned_data.get("site"),
                descricao=form.cleaned_data.get("descricao"),
                logradouro=form.cleaned_data.get("logradouro"),
                bairro=form.cleaned_data.get("bairro"),
                cidade=form.cleaned_data.get("cidade"),
                estado=form.cleaned_data.get("estado"),
                cep=form.cleaned_data.get("cep"),
                setor=form.cleaned_data.get("setor"),
                tamanho_empresa=form.cleaned_data.get("tamanho_empresa"),
                logo=form.cleaned_data.get("logo"),
            )

            messages.success(request, "Empresa cadastrada com sucesso!")
            return redirect("usuarios:login")

        messages.error(request, "Verifique os campos e tente novamente.")
    return redirect("usuarios:cadastro")


# =====================================================
# CADASTRO DE COORDENAÇÃO
# =====================================================
def cadastro_coord(request):
    if request.method == "POST":
        form = CoordenacaoForm(request.POST)
        if form.is_valid():
            senha = form.cleaned_data.get("senha")
            confirmar_senha = form.cleaned_data.get("confirmar_senha")

            if senha != confirmar_senha:
                messages.error(request, "As senhas não coincidem.")
                return redirect("usuarios:cadastro")

            usuario = Usuario.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=senha,
                tipo="coordenador",
                is_staff=True,  # coord pode acessar admin
            )

            Coordenador.objects.create(
                usuario=usuario,
                setor=form.cleaned_data.get("setor", "")
            )

            messages.success(request, "Coordenação cadastrada com sucesso!")
            return redirect("usuarios:login")

        messages.error(request, "Verifique os campos e tente novamente.")
    return redirect("usuarios:cadastro")


# =====================================================
# DASHBOARDS
# =====================================================
@login_required
def dashboard(request):
    user = request.user
    if hasattr(user, "aluno"):
        return redirect("usuarios:dashboard_aluno")
    elif hasattr(user, "empresa"):
        return redirect("usuarios:dashboard_empresa")
    elif hasattr(user, "coordenador"):
        return redirect("usuarios:dashboard_coord")
    return render(request, "usuarios/dashboard.html")


@login_required
def dashboard_aluno(request):
    return render(request, "usuarios/dashboard_aluno.html")


@login_required
def dashboard_empresa(request):
    return render(request, "usuarios/dashboard_empresa.html")


@login_required
def dashboard_coord(request):
    return render(request, "usuarios/dashboard_coord.html")
