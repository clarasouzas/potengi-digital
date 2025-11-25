# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.apps import apps
from django.utils import timezone
from linkif.forms import VagaForm
from usuarios.forms import (
    AlunoEditForm, EmpresaEditForm, CoordenadorEditForm,
    UsuarioEditFormSimples
)

# Models (carregados dinamicamente para evitar import cycles)
User = apps.get_model("usuarios", "Usuario")
Aluno = apps.get_model("usuarios", "Aluno")
Empresa = apps.get_model("usuarios", "Empresa")
Coordenador = apps.get_model("usuarios", "Coordenador")

Vaga = apps.get_model("linkif", "Vaga")
Candidatura = apps.get_model("linkif", "Candidatura")


# ======================================================================
# AVATAR
# ======================================================================
def get_avatar_data(user):
    try:
        if user.tipo == "aluno":
            perfil = user.aluno
            foto = perfil.foto.url if perfil.foto else None
            icone = "bi-person-circle"
        elif user.tipo == "empresa":
            perfil = user.empresa
            foto = perfil.foto.url if hasattr(perfil, "foto") and perfil.foto else None
            icone = "bi-building"
        else:
            perfil = user.coordenador
            foto = perfil.foto.url if hasattr(perfil, "foto") and perfil.foto else None
            icone = "bi-person-badge"
    except:
        foto = None
        icone = "bi-person-circle"
    return foto, icone


# ======================================================================
# MENU DINÂMICO
# ======================================================================
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
            ("dashboard:aprovar_vagas", "bi bi-check2-circle", "Aprovar Vagas"),
            ("dashboard:usuarios", "bi bi-people", "Gerenciar Usuários"),
            ("dashboard:empresas", "bi bi-building", "Gerenciar Empresas"),
            ("dashboard:relatorios", "bi bi-bar-chart", "Relatórios"),
        ]

    return []


# ======================================================================
# REDIRECIONAMENTO PÓS-LOGIN
# ======================================================================
@login_required
def redirecionar_dashboard(request):
    u = request.user
    if u.tipo == "aluno":
        return redirect("dashboard:aluno_painel")
    if u.tipo == "empresa":
        return redirect("dashboard:empresa_painel")
    return redirect("dashboard:coordenacao_painel")


# ======================================================================
# ALUNO
# ======================================================================
@login_required
def aluno_painel(request):
    foto, icone = get_avatar_data(request.user)
    vagas = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")[:6]

    return render(request, "dashboard/aluno/painel.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def aluno_vagas(request):
    foto, icone = get_avatar_data(request.user)
    vagas = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")

    return render(request, "dashboard/aluno/vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def aluno_candidaturas(request):
    foto, icone = get_avatar_data(request.user)
    lista = Candidatura.objects.filter(aluno=request.user.aluno).order_by("-data_candidatura")

    return render(request, "dashboard/aluno/candidaturas.html", {
        "menu": get_menu(request.user),
        "candidaturas": lista,
        "foto": foto,
        "icone": icone,
    })


# ======================================================================
# EMPRESA — VAGAS
# ======================================================================
@login_required
def empresa_painel(request):
    foto, icone = get_avatar_data(request.user)
    vagas = Vaga.objects.filter(empresa=request.user.empresa).order_by("-id")

    return render(request, "dashboard/empresa/painel.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def empresa_vagas(request):
    foto, icone = get_avatar_data(request.user)
    vagas = Vaga.objects.filter(empresa=request.user.empresa).order_by("-id")

    return render(request, "dashboard/empresa/minhas_vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })

@login_required
def empresa_cadastrar_vaga(request):
    foto, icone = get_avatar_data(request.user)

    if not request.user.is_approved:
        messages.warning(request, "Você ainda não pode cadastrar vagas. Aguarde aprovação.")
        return redirect("dashboard:empresa_painel")

    form = VagaForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user.empresa
            vaga.status = "pendente"
            vaga.data_publicacao = None
            vaga.save()

            messages.success(request, "Vaga cadastrada e enviada para aprovação.")
            return redirect("dashboard:empresa_vagas")

        messages.error(request, "Preencha todos os campos obrigatórios.")

    return render(request, "dashboard/empresa/cadastrar_vaga.html", {
        "menu": get_menu(request.user),
        "foto": foto,
        "icone": icone,
        "form": form
    })

@login_required
def empresa_editar_vaga(request, vaga_id):
    foto, icone = get_avatar_data(request.user)
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user.empresa)

    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        descricao = request.POST.get("descricao", "").strip()

        if not titulo or not descricao:
            messages.error(request, "Preencha todos os campos obrigatórios.")
        else:
            vaga.titulo = titulo
            vaga.descricao = descricao
            vaga.status = "pendente"
            vaga.save()
            messages.success(request, "Vaga atualizada e reenviada para aprovação.")
            return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/editar_vaga.html", {
        "menu": get_menu(request.user),
        "vaga": vaga,
        "foto": foto,
        "icone": icone,
    })


@login_required
def empresa_excluir_vaga(request, vaga_id):
    foto, icone = get_avatar_data(request.user)
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user.empresa)

    if request.method == "POST":
        vaga.delete()
        messages.success(request, "Vaga excluída com sucesso.")
        return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/confirmar_exclusao.html", {
        "menu": get_menu(request.user),
        "vaga": vaga,
        "foto": foto,
        "icone": icone,
    })


@login_required
def empresa_candidaturas(request):
    foto, icone = get_avatar_data(request.user)
    candidaturas = Candidatura.objects.filter(vaga__empresa=request.user.empresa).order_by("-data_candidatura")

    return render(request, "dashboard/empresa/candidaturas_recebidas.html", {
        "menu": get_menu(request.user),
        "candidaturas": candidaturas,
        "foto": foto,
        "icone": icone,
    })


# ======================================================================
# COORDENAÇÃO — PAINEL PRINCIPAL
# ======================================================================
@login_required
def coordenacao_painel(request):
    foto, icone = get_avatar_data(request.user)
    return render(request, "dashboard/coordenacao/painel.html", {
        "menu": get_menu(request.user),
        "foto": foto,
        "icone": icone,
    })


# ======================================================================
# COORDENAÇÃO — APROVAÇÃO DE ALUNOS
# ======================================================================
@login_required
def aprovar_alunos(request):
    foto, icone = get_avatar_data(request.user)

    alunos = User.objects.filter(
        tipo="aluno",
        is_approved=False
    ).order_by("id")

    return render(request, "dashboard/coordenacao/aprovar_alunos.html", {
        "menu": get_menu(request.user),
        "alunos": alunos,
        "foto": foto,
        "icone": icone,
    })


# ======================================================================
# COORDENAÇÃO — APROVAÇÃO DE EMPRESAS
# ======================================================================
@login_required
def aprovar_empresas(request):
    foto, icone = get_avatar_data(request.user)

    empresas = User.objects.filter(
        tipo="empresa",
        is_approved=False
    ).order_by("id")

    return render(request, "dashboard/coordenacao/aprovar_empresas.html", {
        "menu": get_menu(request.user),
        "empresas": empresas,
        "foto": foto,
        "icone": icone,
    })


# ======================================================================
# COORDENAÇÃO — APROVAÇÃO DE VAGAS
# ======================================================================
@login_required
def aprovar_vagas(request):
    foto, icone = get_avatar_data(request.user)

    vagas = Vaga.objects.filter(
        status="pendente"
    ).order_by("-data_publicacao", "-id")

    return render(request, "dashboard/coordenacao/aprovar_vagas.html", {
        "menu": get_menu(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


# ======================================================================
# COORDENAÇÃO — AÇÕES EM VAGAS
# ======================================================================
@login_required
def aprovar_vaga_action(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    vaga.status = "aprovada"
    vaga.data_publicacao = timezone.now()  # publica oficialmente
    vaga.aprovado_por = getattr(request.user, "coordenador", None)
    vaga.save()

    messages.success(request, "A vaga foi aprovada e publicada com sucesso!")
    return redirect("dashboard:aprovar_vagas")


@login_required
def reprovar_vaga_action(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    vaga.status = "reprovada"
    vaga.save()

    messages.warning(request, "A vaga foi reprovada com sucesso.")
    return redirect("dashboard:aprovar_vagas")


# ======================================================================
# PERFIL
# ======================================================================
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
    foto, icone = get_avatar_data(request.user)

    if user.tipo == "aluno":
        perfil = user.aluno
        form_class = AlunoEditForm
    elif user.tipo == "empresa":
        perfil = user.empresa
        form_class = EmpresaEditForm
    else:
        perfil = user.coordenador
        form_class = CoordenadorEditForm

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("dashboard:meu_perfil")
        messages.error(request, "Corrija os erros no formulário.")
    else:
        form = form_class(instance=perfil)

    return render(request, "dashboard/editar_perfil.html", {
        "menu": get_menu(request.user),
        "form": form,
        "perfil": perfil,
        "foto": foto,
        "icone": icone,
    })


# ======================================================================
# USUÁRIOS — COORDENAÇÃO
# ======================================================================
@login_required
def coordenacao_usuarios(request):
    foto, icone = get_avatar_data(request.user)
    lista = User.objects.all().order_by("-id")

    return render(request, "dashboard/coordenacao/usuarios_list.html", {
        "menu": get_menu(request.user),
        "usuarios": lista,
        "foto": foto,
        "icone": icone,
    })


@login_required
def coordenacao_usuario_editar(request, user_id):
    foto, icone = get_avatar_data(request.user)
    usuario = get_object_or_404(User, id=user_id)

    form = UsuarioEditFormSimples(request.POST or None, instance=usuario)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("dashboard:usuarios")
        messages.error(request, "Corrija os erros no formulário.")

    return render(request, "dashboard/coordenacao/usuarios_editar.html", {
        "menu": get_menu(request.user),
        "form": form,
        "usuario": usuario,
        "foto": foto,
        "icone": icone,
    })


@login_required
def coordenacao_usuario_excluir(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    messages.success(request, "Usuário removido com sucesso.")
    return redirect("dashboard:usuarios")


# ======================================================================
# EMPRESAS — COORDENAÇÃO
# ======================================================================
@login_required
def coordenacao_empresas(request):
    foto, icone = get_avatar_data(request.user)
    empresas = Empresa.objects.all().order_by("-id")

    return render(request, "dashboard/coordenacao/empresas_list.html", {
        "menu": get_menu(request.user),
        "empresas": empresas,
        "foto": foto,
        "icone": icone,
    })


@login_required
def coordenacao_empresa_editar(request, empresa_id):
    foto, icone = get_avatar_data(request.user)
    empresa = get_object_or_404(Empresa, id=empresa_id)
    form = EmpresaEditForm(request.POST or None, request.FILES or None, instance=empresa)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa atualizada com sucesso.")
            return redirect("dashboard:empresas")
        messages.error(request, "Corrija os erros no formulário.")

    return render(request, "dashboard/coordenacao/empresas_editar.html", {
        "menu": get_menu(request.user),
        "form": form,
        "empresa": empresa,
        "foto": foto,
        "icone": icone,
    })


@login_required
def coordenacao_empresa_excluir(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    empresa.delete()
    messages.success(request, "Empresa removida com sucesso.")
    return redirect("dashboard:empresas")


# ======================================================================
# RELATÓRIOS
# ======================================================================
@login_required
def relatorios(request):
    foto, icone = get_avatar_data(request.user)
    return render(request, "dashboard/coordenacao/relatorios.html", {
        "menu": get_menu(request.user),
        "foto": foto,
        "icone": icone,
    })


