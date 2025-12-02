# dashboard/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from linkif.models import PerfilFormacao, Competencia, AreaAtuacaoPerfil,Vaga, Candidatura
from linkif.forms import PerfilFormacaoForm, CompetenciaForm, AreaAtuacaoForm,VagaForm

from usuarios.models import Usuario

from usuarios.forms import (
    AlunoEditForm,
    EmpresaEditForm,
    CoordenadorEditForm,
    UsuarioEditFormSimples
)

from django.shortcuts import redirect
from django.contrib import messages

def requer_aprovacao(tipo):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = request.user

            # garante que é o tipo correto
            if user.tipo != tipo:
                messages.error(request, "Acesso negado.")
                return redirect("dashboard:inicio")

            # verifica aprovação
            if not user.is_approved:
                messages.warning(request, "Aguarde aprovação para acessar esta área.")
                if tipo == "aluno":
                    return redirect("dashboard:aluno_painel")
                else:
                    return redirect("dashboard:empresa_painel")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator

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
        "vagas": vagas,
        "candidaturas_ativas": candidaturas_ativas,
        "candidaturas_ultimas": candidaturas_ultimas,
        "recomendadas": recomendadas,
    })
@login_required
@user_passes_test(lambda u: u.tipo == "aluno")
@requer_aprovacao("aluno")
def aluno_candidaturas(request):

    candidaturas = Candidatura.objects.filter(
        aluno=request.user
    ).order_by("-data_candidatura")

    return render(request, "dashboard/aluno/candidaturas.html", {
        "candidaturas": candidaturas,
    })
@login_required
@user_passes_test(lambda u: u.tipo == "aluno")
@requer_aprovacao("aluno")
def cancelar_candidatura(request, cand_id):

    candidatura = get_object_or_404(Candidatura, id=cand_id, aluno=request.user)

    if request.method == "POST":
        candidatura.delete()
        messages.success(request, "Candidatura cancelada com sucesso.")
        return redirect("dashboard:aluno_candidaturas")

    return render(request, "dashboard/aluno/cancelar_candidatura.html", {
        "candidatura": candidatura,
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

    return render(request, "dashboard/empresa/painel.html", {
        "total_vagas": total_vagas,
        "vagas_pendentes": vagas_pendentes,
        "total_candidaturas": total_candidaturas,
        "vagas_recentes": vagas_recentes,
    })

@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
@requer_aprovacao("empresa")
def empresa_vagas(request):
    vagas = Vaga.objects.filter(empresa=request.user).order_by("-id")

    return render(request, "dashboard/empresa/minhas_vagas.html", {
        "vagas": vagas,
    })

@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
@requer_aprovacao("empresa")
def empresa_cadastrar_vaga(request):

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
        "form": form,
    })

@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
@requer_aprovacao("empresa")
def empresa_editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)

    form = VagaForm(request.POST or None, instance=vaga)

    if request.method == "POST":
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.status = "pendente"
            vaga.save()
            messages.success(request, "Vaga atualizada e reenviada para aprovação.")
            return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/editar_vaga.html", {
        "form": form,
        "vaga": vaga,
    })
@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
@requer_aprovacao("empresa")
def empresa_excluir_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)

    if request.method == "POST":
        vaga.delete()
        messages.success(request, "Vaga excluída com sucesso.")
        return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/confirmar_exclusao.html", {
        "vaga": vaga,
    })
@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
@requer_aprovacao("empresa")
def empresa_candidaturas(request):
    candidaturas = Candidatura.objects.filter(
        vaga__empresa=request.user
    ).order_by("-data_candidatura")

    return render(request, "dashboard/empresa/candidaturas_recebidas.html", {
        "candidaturas": candidaturas,
    })
@login_required
@user_passes_test(lambda u: u.tipo == "empresa")
@requer_aprovacao("empresa")
def empresa_candidatura_detalhe(request, cand_id):
    candidatura = get_object_or_404(
        Candidatura,
        id=cand_id,
        vaga__empresa=request.user
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

    return render(request, "dashboard/empresa/candidatura_detalhe.html", {
        "candidatura": candidatura,
    })

# ===========================================================
# COORDENAÇÃO
# ===========================================================

def is_coordenador(user):
    return user.is_authenticated and user.tipo == "coordenador"


@login_required
@user_passes_test(is_coordenador)
def coordenacao_painel(request):

    dados = {
        "alunos_pendentes": Usuario.objects.filter(tipo="aluno", is_approved=False).count(),
        "empresas_pendentes": Usuario.objects.filter(tipo="empresa", is_approved=False).count(),
        "vagas_pendentes": Vaga.objects.filter(status="pendente").count(),
        "total_usuarios": Usuario.objects.count(),
        "total_alunos": Usuario.objects.filter(tipo="aluno").count(),
        "total_empresas": Usuario.objects.filter(tipo="empresa").count(),
        "total_vagas": Vaga.objects.count(),
    }

    return render(request, "dashboard/coordenacao/painel.html", dados)


# ------------------------ Aprovar Alunos ------------------------

@login_required
@user_passes_test(is_coordenador)
def aprovar_alunos(request):
    alunos = Usuario.objects.filter(tipo="aluno", is_approved=False)
    return render(request, "dashboard/coordenacao/aprovar_alunos.html", {
        "alunos": alunos
    })


@login_required
@user_passes_test(is_coordenador)
def aprovar_aluno_action(request, user_id):
    aluno = get_object_or_404(Usuario, id=user_id, tipo="aluno")
    aluno.is_approved = True
    aluno.save()
    messages.success(request, "Aluno aprovado com sucesso.")
    return redirect("dashboard:aprovar_alunos")


# ------------------------ Aprovar Empresas ------------------------

@login_required
@user_passes_test(is_coordenador)
def aprovar_empresas(request):
    empresas = Usuario.objects.filter(tipo="empresa", is_approved=False)
    return render(request, "dashboard/coordenacao/aprovar_empresas.html", {
        "empresas": empresas
    })


@login_required
@user_passes_test(is_coordenador)
def aprovar_empresa_action(request, user_id):
    empresa = get_object_or_404(Usuario, id=user_id, tipo="empresa")
    empresa.is_approved = True
    empresa.save()
    messages.success(request, "Empresa aprovada com sucesso.")
    return redirect("dashboard:aprovar_empresas")


# ------------------------ Aprovar Vagas ------------------------

@login_required
@user_passes_test(is_coordenador)
def aprovar_vagas(request):
    vagas = Vaga.objects.filter(status="pendente").order_by("-id")
    return render(request, "dashboard/coordenacao/aprovar_vagas.html", {
        "vagas": vagas
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
def reprovar_vaga_action(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    vaga.status = "reprovada"
    vaga.save()
    messages.warning(request, "Vaga reprovada.")
    return redirect("dashboard:aprovar_vagas")


# ------------------------ Empresas (CRUD simples) ------------------------

@login_required
@user_passes_test(is_coordenador)
def coordenacao_empresas(request):
    empresas = Usuario.objects.filter(tipo="empresa").order_by("-id")
    return render(request, "dashboard/coordenacao/empresas_list.html", {
        "empresas": empresas
    })


@login_required
@user_passes_test(is_coordenador)
def coordenacao_empresa_editar(request, empresa_id):
    empresa = get_object_or_404(Usuario, id=empresa_id, tipo="empresa")
    form = UsuarioEditFormSimples(request.POST or None, instance=empresa)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa atualizada com sucesso.")
            return redirect("dashboard:empresas")
        messages.error(request, "Corrija os erros do formulário.")

    return render(request, "dashboard/coordenacao/empresa_editar.html", {
        "form": form,
        "empresa": empresa
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
    usuarios = Usuario.objects.all().order_by("-id")
    return render(request, "dashboard/coordenacao/usuarios_list.html", {
        "usuarios": usuarios
    })


@login_required
@user_passes_test(is_coordenador)
def coordenacao_usuario_editar(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    form = UsuarioEditFormSimples(request.POST or None, instance=usuario)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("dashboard:usuarios")
        messages.error(request, "Erros no formulário.")

    return render(request, "dashboard/coordenacao/usuarios_editar.html", {
        "form": form,
        "usuario": usuario
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
# PERFIL (do próprio usuário)
# ===========================================================

@login_required
def meu_perfil(request):
    return render(request, "dashboard/meu_perfil.html", {
        "perfil": request.user
    })


@login_required
def editar_perfil(request):
    u = request.user

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
        messages.error(request, "Corrija os erros.")

    return render(request, "dashboard/editar_perfil.html", {
        "form": form
    })


# ===========================================================
# PERFIS DE FORMAÇÃO
# ===========================================================

@login_required
@user_passes_test(is_coordenador)
def listar_perfis(request):
    perfis = PerfilFormacao.objects.all()
    return render(request, "dashboard/coordenacao/perfis_lista.html", {
        "perfis": perfis
    })


@login_required
@user_passes_test(is_coordenador)
def editar_perfil_formacao(request, pk=None):

    perfil = get_object_or_404(PerfilFormacao, pk=pk) if pk else None

    if request.method == "POST":
        form = PerfilFormacaoForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            messages.success(request, "Perfil salvo com sucesso!")
            return redirect("dashboard:editar_perfil_formacao", pk=perfil.pk)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = PerfilFormacaoForm(instance=perfil)

    competencias = Competencia.objects.filter(perfil=perfil) if perfil else []
    areas = AreaAtuacaoPerfil.objects.filter(perfil=perfil) if perfil else []

    return render(request, "dashboard/coordenacao/perfil_form.html", {
        "form": form,
        "perfil": perfil,
        "competencias": competencias,
        "areas": areas,
    })



@login_required
@user_passes_test(is_coordenador)
def excluir_perfil_formacao(request, pk):
    perfil = get_object_or_404(PerfilFormacao, pk=pk)
    perfil.delete()
    messages.success(request, "Perfil removido com sucesso.")
    return redirect("dashboard:listar_perfis")


@login_required
@user_passes_test(is_coordenador)
def adicionar_competencia(request, perfil_id):
    perfil = get_object_or_404(PerfilFormacao, pk=perfil_id)

    if request.method == "POST":
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.perfil = perfil
            comp.save()
            return redirect("dashboard:editar_perfil_formacao", pk=perfil.id)


@login_required
@user_passes_test(is_coordenador)
def remover_competencia(request, pk):
    comp = get_object_or_404(Competencia, pk=pk)
    perfil_id = comp.perfil.id
    comp.delete()
    return redirect("dashboard:editar_perfil_formacao", pk=perfil_id)


@login_required
@user_passes_test(is_coordenador)
def adicionar_area(request, perfil_id):
    perfil = get_object_or_404(PerfilFormacao, pk=perfil_id)

    if request.method == "POST":
        form = AreaAtuacaoForm(request.POST)
        if form.is_valid():
            area = form.save(commit=False)
            area.perfil = perfil
            area.save()
            return redirect("dashboard:editar_perfil_formacao", pk=perfil.id)


@login_required
@user_passes_test(is_coordenador)
def remover_area(request, pk):
    area = get_object_or_404(AreaAtuacaoPerfil, pk=pk)
    perfil_id = area.perfil.id
    area.delete()
    return redirect("dashboard:editar_perfil_formacao", pk=perfil_id)


# ===========================================================
# RELATÓRIOS
# ===========================================================

@login_required
@user_passes_test(is_coordenador)
def relatorios(request):
    return render(request, "dashboard/coordenacao/relatorios.html")
