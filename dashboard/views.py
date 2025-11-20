from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps
from usuarios.forms import AlunoEditForm, EmpresaEditForm, CoordenadorEditForm


# MODELS
User = apps.get_model("usuarios", "Usuario")
Aluno = apps.get_model("usuarios", "Aluno")
Empresa = apps.get_model("usuarios", "Empresa")
Coordenador = apps.get_model("usuarios", "Coordenador")

Vaga = apps.get_model("linkif", "Vaga")
Candidatura = apps.get_model("linkif", "Candidatura")


# =========================================
# FUNÇÃO PARA PEGAR AVATAR (foto ou ícone)
# =========================================
def get_avatar_data(user):
    if user.tipo == "aluno":
        perfil = user.aluno
        foto = perfil.foto.url if perfil.foto else None
        icone = "bi-person-circle"

    elif user.tipo == "empresa":
        perfil = user.empresa
        foto = perfil.foto.url if hasattr(perfil, "foto") and perfil.foto else None
        icone = "bi-building"

    else:  # coordenador
        perfil = user.coordenador
        foto = perfil.foto.url if hasattr(perfil, "foto") and perfil.foto else None
        icone = "bi-person-badge"

    return foto, icone


# =========================================
# MENU DINÂMICO
# =========================================
def get_menu(user):

    if user.tipo == "aluno":
        return [
            ("dashboard:aluno_painel", "bi bi-house-door", "Meu painel"),
            ("dashboard:aluno_candidaturas", "bi bi-file-earmark-check", "Minhas Candidaturas"),
        ]

    if user.tipo == "empresa":
        return [
            ("dashboard:empresa_painel", "bi bi-house-door", "Meu painel"),
            ("dashboard:empresa_vagas", "bi bi-briefcase", "Minhas Vagas"),
            ("dashboard:empresa_cadastrar_vaga", "bi bi-plus-circle", "Cadastrar Vaga"),
            ("dashboard:empresa_candidaturas", "bi bi-people", "Candidaturas Recebidas"),
        ]

    if user.tipo == "coordenador":
        return [
            ("dashboard:coordenacao_painel", "bi bi-house-door", "Meu painel"),
            ("dashboard:aprovar_alunos", "bi bi-person-check", "Aprovar Alunos"),
            ("dashboard:aprovar_empresas", "bi bi-building-check", "Aprovar Empresas"),
            ("dashboard:aprovar_vagas", "bi bi-briefcase-check", "Aprovar Vagas"),
            ("dashboard:usuarios", "bi bi-people", "Gerenciar Usuários"),
            ("dashboard:relatorios", "bi bi-bar-chart", "Relatórios"),
        ]

    return []


# =========================================
# REDIRECIONAMENTO PÓS-LOGIN
# =========================================
@login_required
def redirecionar_dashboard(request):
    user = request.user

    if user.tipo == "aluno":
        return redirect("dashboard:aluno_painel")
    if user.tipo == "empresa":
        return redirect("dashboard:empresa_painel")
    if user.tipo == "coordenador":
        return redirect("dashboard:coordenacao_painel")

    return redirect("index")


# =========================================
# ALUNO
# =========================================
@login_required
def aluno_painel(request):
    foto, icone = get_avatar_data(request.user)
    vagas = Vaga.objects.filter(status="aprovada")[:6]

    return render(request, "dashboard/aluno/painel.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def aluno_vagas(request):
    foto, icone = get_avatar_data(request.user)
    vagas = Vaga.objects.filter(status="aprovada")

    return render(request, "dashboard/aluno/vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def aluno_candidaturas(request):
    foto, icone = get_avatar_data(request.user)
    aluno = request.user.aluno
    candidaturas = Candidatura.objects.filter(aluno=aluno)

    return render(request, "dashboard/aluno/candidaturas.html", {
        "menu": get_menu(request.user),
        "candidaturas": candidaturas,
        "foto": foto,
        "icone": icone,
    })


# =========================================
# EMPRESA
# =========================================
@login_required
def empresa_painel(request):
    foto, icone = get_avatar_data(request.user)
    empresa = request.user.empresa
    vagas = Vaga.objects.filter(empresa=empresa)

    return render(request, "dashboard/empresa/painel.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def empresa_vagas(request):
    foto, icone = get_avatar_data(request.user)
    empresa = request.user.empresa
    vagas = Vaga.objects.filter(empresa=empresa)

    return render(request, "dashboard/empresa/minhas_vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def empresa_cadastrar_vaga(request):
    foto, icone = get_avatar_data(request.user)

    if request.method == "POST":
        Vaga.objects.create(
            titulo=request.POST.get("titulo"),
            descricao=request.POST.get("descricao"),
            empresa=request.user.empresa,
            status="pendente",
        )
        return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/cadastrar_vaga.html", {
        "menu": get_menu(request.user),
        "foto": foto,
        "icone": icone,
    })


@login_required
def empresa_candidaturas(request):
    foto, icone = get_avatar_data(request.user)
    lista = Candidatura.objects.filter(vaga__empresa=request.user.empresa)

    return render(request, "dashboard/empresa/candidaturas_recebidas.html", {
        "menu": get_menu(request.user),
        "candidaturas": lista,
        "foto": foto,
        "icone": icone,
    })


# =========================================
# COORDENAÇÃO
# =========================================
@login_required
def coordenacao_painel(request):
    foto, icone = get_avatar_data(request.user)

    return render(request, "dashboard/coordenacao/painel.html", {
        "menu": get_menu(request.user),
        "foto": foto,
        "icone": icone,
    })


@login_required
def aprovar_alunos(request):
    foto, icone = get_avatar_data(request.user)
    alunos = User.objects.filter(tipo="aluno", is_approved=False)

    return render(request, "dashboard/coordenacao/aprovar_alunos.html", {
        "menu": get_menu(request.user),
        "alunos": alunos,
        "foto": foto,
        "icone": icone,
    })


@login_required
def aprovar_empresas(request):
    foto, icone = get_avatar_data(request.user)
    empresas = User.objects.filter(tipo="empresa", is_approved=False)

    return render(request, "dashboard/coordenacao/aprovar_empresas.html", {
        "menu": get_menu(request.user),
        "empresas": empresas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def aprovar_vagas(request):
    foto, icone = get_avatar_data(request.user)
    vagas = Vaga.objects.filter(status="pendente")

    return render(request, "dashboard/coordenacao/aprovar_vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def usuarios(request):
    foto, icone = get_avatar_data(request.user)
    lista = User.objects.all()

    return render(request, "dashboard/coordenacao/usuarios.html", {
        "menu": get_menu(request.user),
        "usuarios": lista,
        "foto": foto,
        "icone": icone,
    })


@login_required
def relatorios(request):
    foto, icone = get_avatar_data(request.user)

    return render(request, "dashboard/coordenacao/relatorios.html", {
        "menu": get_menu(request.user),
        "foto": foto,
        "icone": icone,
    })

@login_required
def meu_perfil(request):
    foto, icone = get_avatar_data(request.user)

    if request.user.tipo == "aluno":
        perfil = request.user.aluno
    elif request.user.tipo == "empresa":
        perfil = request.user.empresa
    else:
        perfil = request.user.coordenador

    return render(request, "dashboard/meu_perfil.html", {
        "menu": get_menu(request.user),
        "perfil": perfil,
        "foto": foto,
        "icone": icone,
        "user": request.user,
    })

@login_required
def editar_perfil(request):

    user = request.user
    foto, icone = get_avatar_data(user)

    # Selecionar form conforme o tipo
    if user.tipo == "aluno":
        perfil = user.aluno
        form_class = AlunoEditForm

    elif user.tipo == "empresa":
        perfil = user.empresa
        form_class = EmpresaEditForm

    else:  # coordenador
        perfil = user.coordenador
        form_class = CoordenadorEditForm

    # POST
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("dashboard:inicio")

    else:
        form = form_class(instance=perfil)

    return render(request, "dashboard/editar_perfil.html", {
        "menu": get_menu(user),
        "form": form,
        "foto": foto,
        "icone": icone,
        "perfil": perfil,
        "user": user,
    })
