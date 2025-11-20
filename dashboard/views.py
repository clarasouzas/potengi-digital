from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps

# MODELS
User = apps.get_model("usuarios", "Usuario")
Aluno = apps.get_model("usuarios", "Aluno")
Empresa = apps.get_model("usuarios", "Empresa")
Coordenador = apps.get_model("usuarios", "Coordenador")

Vaga = apps.get_model("linkif", "Vaga")
Candidatura = apps.get_model("linkif", "Candidatura")


# =========================================
# MENU DINÂMICO
# =========================================
def get_menu(user):

    if user.tipo == "aluno":
        return [
            ("dashboard:aluno_painel", "bi bi-speedometer2", "Início"),
            ("dashboard:aluno_vagas", "bi bi-briefcase", "Vagas"),
            ("dashboard:aluno_candidaturas", "bi bi-file-earmark-check", "Minhas Candidaturas"),
        ]

    if user.tipo == "empresa":
        return [
            ("dashboard:empresa_painel", "bi bi-speedometer2", "Início"),
            ("dashboard:empresa_vagas", "bi bi-briefcase", "Minhas Vagas"),
            ("dashboard:empresa_cadastrar_vaga", "bi bi-plus-circle", "Cadastrar Vaga"),
            ("dashboard:empresa_candidaturas", "bi bi-people", "Candidaturas Recebidas"),
        ]

    if user.tipo == "coordenador":
        return [
            ("dashboard:coordenacao_painel", "bi bi-speedometer2", "Início"),
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
    vagas = Vaga.objects.filter(status="aprovada")[:6]
    return render(request, "dashboard/aluno/painel.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
    })


@login_required
def aluno_vagas(request):
    vagas = Vaga.objects.filter(status="aprovada")
    return render(request, "dashboard/aluno/vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
    })


@login_required
def aluno_candidaturas(request):
    aluno = request.user.aluno
    candidaturas = Candidatura.objects.filter(aluno=aluno)
    return render(request, "dashboard/aluno/candidaturas.html", {
        "menu": get_menu(request.user),
        "candidaturas": candidaturas,
    })


# =========================================
# EMPRESA
# =========================================
@login_required
def empresa_painel(request):
    empresa = request.user.empresa
    vagas = Vaga.objects.filter(empresa=empresa)
    return render(request, "dashboard/empresa/painel.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
    })


@login_required
def empresa_vagas(request):
    empresa = request.user.empresa
    vagas = Vaga.objects.filter(empresa=empresa)
    return render(request, "dashboard/empresa/minhas_vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
    })


@login_required
def empresa_cadastrar_vaga(request):
    if request.method == "POST":
        Vaga.objects.create(
            titulo=request.POST.get("titulo"),
            descricao=request.POST.get("descricao"),
            empresa=request.user.empresa,
            status="pendente",
        )
        return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/cadastrar_vaga.html", {
        "menu": get_menu(request.user)
    })


@login_required
def empresa_candidaturas(request):
    lista = Candidatura.objects.filter(vaga__empresa=request.user.empresa)
    return render(request, "dashboard/empresa/candidaturas_recebidas.html", {
        "menu": get_menu(request.user),
        "candidaturas": lista,
    })


# =========================================
# COORDENAÇÃO
# =========================================
@login_required
def coordenacao_painel(request):
    return render(request, "dashboard/coordenacao/painel.html", {
        "menu": get_menu(request.user),
    })


@login_required
def aprovar_alunos(request):
    alunos = User.objects.filter(tipo="aluno", is_approved=False)
    return render(request, "dashboard/coordenacao/aprovar_alunos.html", {
        "menu": get_menu(request.user),
        "alunos": alunos,
    })


@login_required
def aprovar_empresas(request):
    empresas = User.objects.filter(tipo="empresa", is_approved=False)
    return render(request, "dashboard/coordenacao/aprovar_empresas.html", {
        "menu": get_menu(request.user),
        "empresas": empresas,
    })


@login_required
def aprovar_vagas(request):
    vagas = Vaga.objects.filter(status="pendente")
    return render(request, "dashboard/coordenacao/aprovar_vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
    })


@login_required
def usuarios(request):
    lista = User.objects.all()
    return render(request, "dashboard/coordenacao/usuarios.html", {
        "menu": get_menu(request.user),
        "usuarios": lista,
    })


@login_required
def relatorios(request):
    return render(request, "dashboard/coordenacao/relatorios.html", {
        "menu": get_menu(request.user),
    })


# =========================================
# EDITAR PERFIL
# =========================================
@login_required
def editar_perfil(request):
    return render(request, "dashboard/editar_perfil.html", {
        "menu": get_menu(request.user),
    })
