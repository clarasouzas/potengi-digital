# dashboard/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

from usuarios.models import Usuario
from linkif.models import Vaga, Candidatura
from linkif.forms import VagaForm
from usuarios.forms import (
    AlunoEditForm,
    EmpresaEditForm,
    CoordenadorEditForm,
    UsuarioEditFormSimples
)


# ===========================================================
# FUNÇÕES AUXILIARES
# ===========================================================

def get_avatar(user):
    """
    Sempre retorna: (foto_url ou None, icone_class)
    """
    foto_url = None
    icone = "bi bi-person-circle"

    try:
        if user.foto:
            foto_url = user.foto.url
    except:
        foto_url = None

    if user.tipo == "empresa":
        icone = "bi bi-building"
    elif user.tipo == "coordenador":
        icone = "bi bi-person-badge"
    else:
        icone = "bi bi-person-circle"

    return foto_url, icone


def menu_por_tipo(user):
    if user.tipo == "aluno":
        return [
            ("dashboard:aluno_painel", "bi bi-house", "Meu Painel"),
            ("dashboard:aluno_candidaturas", "bi bi-file-earmark-check", "Minhas Candidaturas"),
        ]

    if user.tipo == "empresa":
        return [
            ("dashboard:empresa_painel", "bi bi-house", "Meu Painel"),
            ("dashboard:empresa_vagas", "bi bi-briefcase", "Minhas Vagas"),
            ("dashboard:empresa_cadastrar_vaga", "bi bi-plus-circle", "Cadastrar Vaga"),
            ("dashboard:empresa_candidaturas", "bi bi-people", "Candidaturas Recebidas"),
        ]

    if user.tipo == "coordenador":
        return [
            ("dashboard:coordenacao_painel", "bi bi-house", "Painel da Coordenação"),
            ("dashboard:aprovar_alunos", "bi bi-person-check", "Aprovar Alunos"),
            ("dashboard:aprovar_empresas", "bi bi-building-check", "Aprovar Empresas"),
            ("dashboard:aprovar_vagas", "bi bi-check2-circle", "Aprovar Vagas"),
            ("dashboard:usuarios", "bi bi-people", "Gerenciar Usuários"),
            ("dashboard:relatorios", "bi bi-bar-chart", "Relatórios"),
        ]

    return []


# ===========================================================
# REDIRECIONAMENTO PÓS-LOGIN
# ===========================================================

@login_required
def inicio(request):
    if request.user.tipo == "aluno":
        return redirect("dashboard:aluno_painel")
    if request.user.tipo == "empresa":
        return redirect("dashboard:empresa_painel")
    return redirect("dashboard:coordenacao_painel")


# ===========================================================
# ALUNO
# ===========================================================

@login_required
@user_passes_test(lambda u: u.tipo == "aluno")
def aluno_painel(request):
    foto, icone = get_avatar(request.user)

    vagas = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")[:6]

    candidaturas_ativas = Candidatura.objects.filter(
        aluno=request.user
    ).exclude(status="recusado")

    candidaturas_ultimas = Candidatura.objects.filter(
        aluno=request.user
    ).order_by("-data_candidatura")[:5]

    recomendadas = Vaga.objects.filter(
        curso__nome=request.user.curso,
        status="aprovada"
    )[:4]

    return render(request, "dashboard/aluno/painel.html", {
        "menu": menu_por_tipo(request.user),
        "foto": foto,
        "icone": icone,
        "vagas": vagas,
        "candidaturas_ativas": candidaturas_ativas,
        "candidaturas_ultimas": candidaturas_ultimas,
        "recomendadas": recomendadas,
    })


@login_required
@user_passes_test(lambda u: u.tipo == "aluno")
def aluno_candidaturas(request):
    foto, icone = get_avatar(request.user)

    candidaturas = Candidatura.objects.filter(
        aluno=request.user
    ).order_by("-data_candidatura")

    return render(request, "dashboard/aluno/candidaturas.html", {
        "menu": menu_por_tipo(request.user),
        "candidaturas": candidaturas,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(lambda u: u.tipo == "aluno")
def cancelar_candidatura(request, cand_id):
    candidatura = get_object_or_404(Candidatura, id=cand_id, aluno=request.user)

    if request.method == "POST":
        candidatura.delete()
        messages.success(request, "Candidatura cancelada com sucesso.")
        return redirect("dashboard:aluno_candidaturas")

    foto, icone = get_avatar(request.user)

    return render(request, "dashboard/aluno/cancelar_candidatura.html", {
        "menu": menu_por_tipo(request.user),
        "candidatura": candidatura,
        "foto": foto,
        "icone": icone,
    })


# ===========================================================
# EMPRESA
# ===========================================================
@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
def empresa_painel(request):
    usuario = request.user

    vagas = Vaga.objects.filter(empresa=usuario)
    vagas_recentes = vagas.order_by("-id")[:6]

    total_vagas = vagas.count()
    vagas_pendentes = vagas.filter(status="pendente").count()
    total_candidaturas = Candidatura.objects.filter(vaga__empresa=usuario).count()

    avatar, icone = get_avatar(usuario)

    return render(request, "dashboard/empresa/painel.html", {
        "menu": menu_por_tipo(usuario),
        "foto": avatar,
        "icone": icone,

        "total_vagas": total_vagas,
        "vagas_pendentes": vagas_pendentes,
        "total_candidaturas": total_candidaturas,
        "vagas_recentes": vagas_recentes,
    })


@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
def empresa_vagas(request):
    foto, icone = get_avatar(request.user)

    vagas = Vaga.objects.filter(empresa=request.user).order_by("-id")

    return render(request, "dashboard/empresa/minhas_vagas.html", {
        "menu": menu_por_tipo(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
def empresa_cadastrar_vaga(request):
    foto, icone = get_avatar(request.user)

    if not request.user.is_approved:
        messages.warning(request, "Aguarde sua empresa ser aprovada pela coordenação.")
        return redirect("dashboard:empresa_painel")

    form = VagaForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user
            vaga.status = "pendente"
            vaga.save()
            messages.success(request, "Vaga enviada para aprovação.")
            return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/cadastrar_vaga.html", {
        "menu": menu_por_tipo(request.user),
        "form": form,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
def empresa_editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    foto, icone = get_avatar(request.user)

    form = VagaForm(request.POST or None, instance=vaga)

    if request.method == "POST":
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.status = "pendente"
            vaga.save()
            messages.success(request, "Vaga atualizada e reenviada para aprovação.")
            return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/editar_vaga.html", {
        "menu": menu_por_tipo(request.user),
        "form": form,
        "vaga": vaga,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
def empresa_excluir_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)

    if request.method == "POST":
        vaga.delete()
        messages.success(request, "Vaga excluída com sucesso.")
        return redirect("dashboard:empresa_vagas")

    foto, icone = get_avatar(request.user)

    return render(request, "dashboard/empresa/confirmar_exclusao.html", {
        "menu": menu_por_tipo(request.user),
        "vaga": vaga,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
def empresa_candidaturas(request):
    foto, icone = get_avatar(request.user)

    candidaturas = Candidatura.objects.filter(
        vaga__empresa=request.user
    ).order_by("-data_candidatura")

    return render(request, "dashboard/empresa/candidaturas_recebidas.html", {
        "menu": menu_por_tipo(request.user),
        "candidaturas": candidaturas,
        "foto": foto,
        "icone": icone,
    })

@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
def empresa_candidatura_detalhe(request, cand_id):
    candidatura = get_object_or_404(
        Candidatura,
        id=cand_id,
        vaga__empresa=request.user  # empresa só vê suas próprias candidaturas
    )

    if request.method == "POST":
        novo_status = request.POST.get("status")

        if novo_status in ["em_analise", "aprovado", "recusado"]:
            candidatura.status = novo_status
            candidatura.save()
            messages.success(request, "Status atualizado com sucesso!")
        else:
            messages.error(request, "Status inválido.")

        return redirect("dashboard:empresa_candidaturas")

    avatar, icone = get_avatar(request.user)

    return render(request, "dashboard/empresa/candidatura_detalhe.html", {
        "menu": menu_por_tipo(request.user),
        "candidatura": candidatura,
        "foto": avatar,
        "icone": icone,
    })

# ===========================================================
# COORDENAÇÃO
# ===========================================================

def is_coordenador(user):
    return user.is_authenticated and user.tipo == "coordenador"


@login_required
@user_passes_test(is_coordenador)
def coordenacao_painel(request):
    foto, icone = get_avatar(request.user)

    dados = {
        "alunos_pendentes": Usuario.objects.filter(tipo="aluno", is_approved=False).count(),
        "empresas_pendentes": Usuario.objects.filter(tipo="empresa", is_approved=False).count(),
        "vagas_pendentes": Vaga.objects.filter(status="pendente").count(),
        "total_usuarios": Usuario.objects.count(),
        "total_alunos": Usuario.objects.filter(tipo="aluno").count(),
        "total_empresas": Usuario.objects.filter(tipo="empresa").count(),
        "total_vagas": Vaga.objects.count(),
    }

    return render(request, "dashboard/coordenacao/painel.html", {
        "menu": menu_por_tipo(request.user),
        "foto": foto,
        "icone": icone,
        **dados,
    })


@login_required
@user_passes_test(is_coordenador)
def aprovar_alunos(request):
    foto, icone = get_avatar(request.user)

    alunos = Usuario.objects.filter(tipo="aluno", is_approved=False)

    return render(request, "dashboard/coordenacao/aprovar_alunos.html", {
        "menu": menu_por_tipo(request.user),
        "alunos": alunos,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(is_coordenador)
def aprovar_empresas(request):
    foto, icone = get_avatar(request.user)

    empresas = Usuario.objects.filter(tipo="empresa", is_approved=False)

    return render(request, "dashboard/coordenacao/aprovar_empresas.html", {
        "menu": menu_por_tipo(request.user),
        "empresas": empresas,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(is_coordenador)
def aprovar_empresa_action(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id, tipo="empresa")
    usuario.is_approved = True
    usuario.save()
    messages.success(request, "Empresa aprovada com sucesso.")
    return redirect("dashboard:aprovar_empresas")


@login_required
@user_passes_test(is_coordenador)
def aprovar_vagas(request):
    foto, icone = get_avatar(request.user)

    vagas = Vaga.objects.filter(status="pendente").order_by("-id")

    return render(request, "dashboard/coordenacao/aprovar_vagas.html", {
        "menu": menu_por_tipo(request.user),
        "vagas": vagas,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(is_coordenador)
def aprovar_vaga_action(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    vaga.status = "aprovada"
    vaga.data_publicacao = timezone.now()
    vaga.aprovado_por = request.user
    vaga.save()
    messages.success(request, "Vaga aprovada e publicada.")
    return redirect("dashboard:aprovar_vagas")
@login_required
@user_passes_test(is_coordenador)
def aprovar_aluno_action(request, user_id):
    aluno = get_object_or_404(Usuario, id=user_id, tipo="aluno")
    aluno.is_approved = True
    aluno.save()
    messages.success(request, "Aluno aprovado com sucesso.")
    return redirect("dashboard:aprovar_alunos")


@login_required
@user_passes_test(is_coordenador)
def reprovar_vaga_action(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    vaga.status = "reprovada"
    vaga.save()
    messages.warning(request, "Vaga reprovada.")
    return redirect("dashboard:aprovar_vagas")

@login_required
@user_passes_test(is_coordenador)
def coordenacao_empresas(request):
    foto, icone = get_avatar(request.user)

    empresas = Usuario.objects.filter(tipo="empresa").order_by("-id")

    return render(request, "dashboard/coordenacao/empresas_list.html", {
        "menu": menu_por_tipo(request.user),
        "empresas": empresas,
        "foto": foto,
        "icone": icone,
    })
@login_required
@user_passes_test(is_coordenador)
def coordenacao_empresa_editar(request, empresa_id):
    foto, icone = get_avatar(request.user)

    empresa = get_object_or_404(Usuario, id=empresa_id, tipo="empresa")

    form = UsuarioEditFormSimples(request.POST or None, instance=empresa)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa atualizada com sucesso.")
            return redirect("dashboard:empresas")
        messages.error(request, "Corrija os erros do formulário.")

    return render(request, "dashboard/coordenacao/empresa_editar.html", {
        "menu": menu_por_tipo(request.user),
        "form": form,
        "empresa": empresa,
        "foto": foto,
        "icone": icone,
    })
@login_required
@user_passes_test(is_coordenador)
def coordenacao_empresa_excluir(request, empresa_id):
    empresa = get_object_or_404(Usuario, id=empresa_id, tipo="empresa")
    empresa.delete()
    messages.success(request, "Empresa removida com sucesso.")
    return redirect("dashboard:empresas")


# ===========================================================
# GERENCIAR USUÁRIOS
# ===========================================================

@login_required
@user_passes_test(is_coordenador)
def coordenacao_usuarios(request):
    foto, icone = get_avatar(request.user)

    usuarios = Usuario.objects.all().order_by("-id")

    return render(request, "dashboard/coordenacao/usuarios_list.html", {
        "menu": menu_por_tipo(request.user),
        "usuarios": usuarios,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(is_coordenador)
def coordenacao_usuario_editar(request, user_id):
    foto, icone = get_avatar(request.user)
    usuario = get_object_or_404(Usuario, id=user_id)

    form = UsuarioEditFormSimples(request.POST or None, instance=usuario)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("dashboard:usuarios")
        messages.error(request, "Erros no formulário.")

    return render(request, "dashboard/coordenacao/usuarios_editar.html", {
        "menu": menu_por_tipo(request.user),
        "usuario": usuario,
        "form": form,
        "foto": foto,
        "icone": icone,
    })


@login_required
@user_passes_test(is_coordenador)
def coordenacao_usuario_excluir(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.delete()
    messages.success(request, "Usuário excluído com sucesso.")
    return redirect("dashboard:usuarios")


@login_required
@user_passes_test(is_coordenador)
def tornar_admin(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    if usuario.is_superuser:
        messages.warning(request, "Este usuário já é administrador.")
        return redirect("dashboard:usuarios")

    usuario.is_superuser = True
    usuario.is_staff = True
    usuario.save()

    messages.success(request, "Usuário promovido a administrador.")
    return redirect("dashboard:usuarios")


# ===========================================================
# PERFIL
# ===========================================================

@login_required
def meu_perfil(request):
    foto, icone = get_avatar(request.user)

    return render(request, "dashboard/meu_perfil.html", {
        "menu": menu_por_tipo(request.user),
        "perfil": request.user,
        "foto": foto,
        "icone": icone,
    })


@login_required
def editar_perfil(request):
    u = request.user
    foto, icone = get_avatar(request.user)

    if u.tipo == "aluno":
        form_class = AlunoEditForm
    elif u.tipo == "empresa":
        form_class = EmpresaEditForm
    else:
        form_class = CoordenadorEditForm

    form = form_class(request.POST or None, request.FILES or None, instance=u)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("dashboard:perfil")
        else:
            messages.error(request, "Corrija os erros.")

    return render(request, "dashboard/editar_perfil.html", {
        "menu": menu_por_tipo(request.user),
        "form": form,
        "foto": foto,
        "icone": icone,
    })


# ===========================================================
# RELATÓRIOS
# ===========================================================

@login_required
@user_passes_test(is_coordenador)
def relatorios(request):
    foto, icone = get_avatar(request.user)

    return render(request, "dashboard/coordenacao/relatorios.html", {
        "menu": menu_por_tipo(request.user),
        "foto": foto,
        "icone": icone,
    })
