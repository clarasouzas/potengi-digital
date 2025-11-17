# usuarios/views.py — versão segura recomendada
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, AlunoEditForm


from .forms import AlunoForm, EmpresaForm, CoordenacaoForm
from .models import Usuario, Aluno, Empresa, Coordenador

# VIEW: perfil do aluno
def perfil_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    return render(request, "usuarios/perfil_aluno.html", {"aluno": aluno})

# LOGOUT
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("usuarios:login")

# CADASTRO GERAL (com abas)
def cadastro(request):
    forms = [
        ("aluno", AlunoForm(), "usuarios:cadastro_aluno", "primary", "bi-mortarboard-fill", "Cadastro de Aluno"),
        ("empresa", EmpresaForm(), "usuarios:cadastro_empresa", "success", "bi-building-fill", "Cadastro de Empresa"),
        ("coord", CoordenacaoForm(), "usuarios:cadastro_coord", "secondary", "bi-person-gear", "Cadastro de Coordenação"),
    ]
    return render(request, "registration/cadastro.html", {"forms": forms})

# CADASTRO DE ALUNO
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
                first_name=form.cleaned_data["nome"],

            )
            Aluno.objects.create(
                usuario=usuario,
                curso=form.cleaned_data["curso"],
            )
            messages.success(request, "Aluno cadastrado com sucesso!")
            return redirect("usuarios:login")
        messages.error(request, "Verifique os campos e tente novamente.")
    return redirect("usuarios:cadastro")

# CADASTRO DE EMPRESA
def cadastro_empresa(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST, request.FILES)
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
                tipo="empresa",
            )
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

# CADASTRO DE COORDENAÇÃO
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
                is_staff=True,
            )
            Coordenador.objects.create(
                usuario=usuario,
                setor=form.cleaned_data.get("setor", "")
            )
            messages.success(request, "Coordenação cadastrada com sucesso!")
            return redirect("usuarios:login")
        messages.error(request, "Verifique os campos e tente novamente.")
    return redirect("usuarios:cadastro")

# DASHBOARDS
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

@login_required
def editar_perfil_aluno(request):
    usuario = request.user
    aluno = request.user.aluno

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=usuario)
        aluno_form = AlunoEditForm(request.POST, request.FILES, instance=aluno)

        if user_form.is_valid() and aluno_form.is_valid():
            user_form.save()
            aluno_form.save()
            return redirect("usuarios:perfil_aluno", id=aluno.id)

    else:
        user_form = UserEditForm(instance=usuario)
        aluno_form = AlunoEditForm(instance=aluno)

    return render(request, "usuarios/editar_perfil_aluno.html", {
        "user_form": user_form,
        "aluno_form": aluno_form
    })
