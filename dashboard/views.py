from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps

# MODELS
User = apps.get_model("usuarios", "Usuario")
Aluno = apps.get_model("usuarios", "Aluno")
Empresa = apps.get_model("usuarios", "Empresa")
Coordenacao = apps.get_model("usuarios", "Coordenador")

Vaga = apps.get_model("linkif", "Vaga")
Candidatura = apps.get_model("linkif", "Candidatura")


# =======================================================
# MENU DINÂMICO POR TIPO DE USUÁRIO
# =======================================================
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


# =======================================================
# REDIRECIONAMENTO APÓS LOGIN
# =======================================================
@login_required
def redirecionar_dashboard(request):
    user = request.user

    if user.tipo == "aluno":
        return redirect("dashboard:aluno_painel")

    if user.tipo == "empresa":
        return redirect("dashboard:empresa_painel")

    if user.tipo == "coordenador":
        return redirect("dashboard:coordenacao_painel")

    return redirect("/")


# =======================================================
# ALUNO
# =======================================================
@login_required
def aluno_painel(request):
    vagas = Vaga.objects.filter(status="aprovada")[:6]
    return render(request, "dashboard/aluno/painel.html", {
        "vagas": vagas,
        "menu": get_menu(request.user)
    })


@login_required
def aluno_vagas(request):
    vagas = Vaga.objects.filter(status="aprovada")
    return render(request, "dashboard/aluno/vagas.html", {
        "vagas": vagas,
        "menu": get_menu(request.user)
    })


@login_required
def aluno_candidaturas(request):
    aluno = request.user.aluno  # pega o perfil aluno ligado ao usuário logado
    lista = Candidatura.objects.filter(aluno=aluno)
    
    return render(request, "dashboard/aluno/candidaturas.html", {
        "candidaturas": lista,
        "menu": get_menu(request.user)
    })

# =======================================================
# EMPRESA
# =======================================================
@login_required
def empresa_painel(request):
    empresa = getattr(request.user, "empresa", None)
    vagas = Vaga.objects.filter(empresa=empresa)
    return render(request, "dashboard/empresa/painel.html", {
        "empresa": empresa,
        "vagas": vagas,
        "menu": get_menu(request.user)
    })


@login_required
def empresa_vagas(request):
    empresa = getattr(request.user, "empresa", None)
    vagas = Vaga.objects.filter(empresa=empresa)
    return render(request, "dashboard/empresa/vagas.html", {
        "vagas": vagas,
        "menu": get_menu(request.user)
    })


@login_required
def empresa_cadastrar_vaga(request):
    if request.method == "POST":
        Vaga.objects.create(
            titulo=request.POST.get("titulo"),
            descricao=request.POST.get("descricao"),
            empresa=request.user.empresa,
            status="pendente"
        )
        return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/cadastrar_vaga.html", {
        "menu": get_menu(request.user)
    })


@login_required
def empresa_candidaturas(request):
    empresa = getattr(request.user, "empresa", None)
    lista = Candidatura.objects.filter(vaga__empresa=empresa)
    return render(request, "dashboard/empresa/candidaturas.html", {
        "candidaturas": lista,
        "menu": get_menu(request.user)
    })


# =======================================================
# COORDENAÇÃO
# =======================================================
@login_required
def coordenacao_painel(request):
    return render(request, "dashboard/coordenacao/painel.html", {
        "menu": get_menu(request.user)
    })


@login_required
def aprovar_alunos(request):
    alunos = User.objects.filter(is_approved=False, tipo="aluno")
    return render(request, "dashboard/coordenacao/aprovar_alunos.html", {
        "alunos": alunos,
        "menu": get_menu(request.user)
    })


@login_required
def aprovar_empresas(request):
    empresas = User.objects.filter(is_approved=False, tipo="empresa")
    return render(request, "dashboard/coordenacao/aprovar_empresas.html", {
        "empresas": empresas,
        "menu": get_menu(request.user)
    })


@login_required
def aprovar_vagas(request):
    vagas = Vaga.objects.filter(status="pendente")
    return render(request, "dashboard/coordenacao/aprovar_vagas.html", {
        "vagas": vagas,
        "menu": get_menu(request.user)
    })


@login_required
def usuarios(request):
    lista = User.objects.all()
    return render(request, "dashboard/coordenacao/usuarios.html", {
        "usuarios": lista,
        "menu": get_menu(request.user)
    })


@login_required
def relatorios(request):
    return render(request, "dashboard/coordenacao/relatorios.html", {
        "menu": get_menu(request.user)
    })


# =======================================================
# EDITAR PERFIL (temporário)
# =======================================================
@login_required
def editar_perfil(request):
    return render(request, "dashboard/editar_perfil.html", {
        "menu": get_menu(request.user)
    })
