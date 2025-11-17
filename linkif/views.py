from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

from .models import (
    Vaga,
    Candidatura,
    Notificacao,
    Mensagem,
    SiteConfig,
    HomeContent,
    AreaAtuacao,
    PerfilFormacao,
)
from .forms import VagaForm, CandidaturaForm, ContatoForm
from usuarios.models import Empresa

# =====================================================
# FUNÇÕES AUXILIARES (controle de acesso)
# =====================================================

def is_coordenador(user):
    return user.is_authenticated and getattr(user, "tipo", None) == "coordenador"

def is_empresa(user):
    return user.is_authenticated and getattr(user, "tipo", None) == "empresa"

def is_aluno(user):
    return user.is_authenticated and getattr(user, "tipo", None) == "aluno"

# =====================================================
# INDEX (home) — dinâmico com SiteConfig e HomeContent
# =====================================================
def index(request):
    site = SiteConfig.objects.first()
    home = HomeContent.objects.first()
    vagas = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")[:6]

    # garante ordem previsível (pelo campo 'ordem' definido no model)
    perfis = list(PerfilFormacao.objects.all().order_by("ordem", "nome"))

    # duplica pra deixar o carrossel circular sem corte
    if len(perfis) > 3:
        perfis = perfis + perfis[:2]

    # formulário de contato
    form = ContatoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Mensagem enviada com sucesso! Entraremos em contato em breve.")
        return redirect("index")

    context = {
        "site": site,
        "home": home,
        "vagas": vagas,
        "perfis": perfis,
        "form": form,
    }
    return render(request, "linkif/index.html", context)

# =====================================================
# VAGAS — listagem, detalhes e criação
# =====================================================
def listar_vagas(request):
    vagas = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")
    areas = AreaAtuacao.objects.all()

    titulo = request.GET.get("titulo")
    area = request.GET.get("area")
    cidade = request.GET.get("cidade")
    tipo = request.GET.get("tipo")

    if titulo:
        vagas = vagas.filter(titulo__icontains=titulo)
    if area:
        vagas = vagas.filter(area__nome__icontains=area)
    if cidade:
        vagas = vagas.filter(cidade__icontains=cidade)
    if tipo:
        vagas = vagas.filter(tipo__iexact=tipo)

    return render(request, "linkif/vagas.html", {"vagas": vagas, "areas": areas})
# =====================================================
# EMPRESA: CRUD DE VAGAS
# =====================================================

@login_required
@user_passes_test(is_empresa)
def criar_vaga(request):
    if request.method == "POST":
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user.empresa
            vaga.status = "pendente"
            vaga.save()
            messages.info(request, "✅ Vaga enviada para aprovação da coordenação.")
            return redirect("listar_vagas_empresa")
    else:
        form = VagaForm()
    return render(request, "dashboard/empresas/criar_vaga.html", {"form": form})


@login_required
@user_passes_test(is_empresa)
def listar_vagas_empresa(request):
    vagas = Vaga.objects.filter(empresa=request.user.empresa)
    return render(request, "dashboard/empresas/listar_vagas_empresa.html", {"vagas": vagas})


@login_required
@user_passes_test(is_empresa)
def editar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id, empresa=request.user.empresa)
    if request.method == "POST":
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Vaga atualizada com sucesso.")
            return redirect("listar_vagas_empresa")
    else:
        form = VagaForm(instance=vaga)
    return render(request, "dashboard/empresas/editar_vaga.html", {"form": form})


@login_required
@user_passes_test(is_empresa)
def excluir_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id, empresa=request.user.empresa)
    vaga.delete()
    messages.warning(request, "🚫 Vaga excluída com sucesso.")
    return redirect("listar_vagas_empresa")


def listar_vagas_publicas(request):
    vagas = Vaga.objects.filter(status="aprovada", ativa=True)
    return render(request, "dashboard/empresas/listar_vagas_publicas.html", {"vagas": vagas})


@login_required
@user_passes_test(is_coordenador)
def aprovar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    vaga.status = "aprovada"
    vaga.aprovado_por = request.user.coordenador
    vaga.save()

    Notificacao.objects.create(
        tipo="Vaga aprovada",
        mensagem=f"Sua vaga '{vaga.titulo}' foi aprovada e publicada.",
        usuario_destino=vaga.empresa.usuario,
    )

    messages.success(request, f"Vaga '{vaga.titulo}' aprovada com sucesso.")
    return redirect("listar_vagas")

# =====================================================
# CANDIDATURA
# =====================================================

@login_required
@user_passes_test(is_aluno)
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, status="aprovada")
    aluno = request.user.aluno

    if Candidatura.objects.filter(vaga=vaga, aluno=aluno).exists():
        messages.warning(request, "Você já se candidatou a esta vaga.")
        return redirect("detalhar_vaga", vaga_id=vaga.id)

    if request.method == "POST":
        form = CandidaturaForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.vaga = vaga
            candidatura.aluno = aluno
            candidatura.data_candidatura = timezone.now()
            candidatura.status = "em_analise"
            candidatura.save()

            # notifica empresa
            Notificacao.objects.create(
                tipo="Nova candidatura",
                mensagem=f"O aluno {aluno.usuario.get_full_name()} se candidatou à vaga '{vaga.titulo}'.",
                usuario_destino=vaga.empresa.usuario,
            )

            messages.success(request, "Candidatura enviada com sucesso!")
            return redirect("listar_vagas")
    else:
        form = CandidaturaForm()

    return render(request, "linkif/candidatar.html", {"form": form, "vaga": vaga})


@login_required
@user_passes_test(is_empresa)
def atualizar_status_candidatura(request, candidatura_id, status):
    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    candidatura.status = status
    candidatura.save()

    Notificacao.objects.create(
        tipo="Atualização de candidatura",
        mensagem=f"Sua candidatura na vaga '{candidatura.vaga.titulo}' foi marcada como {status}.",
        usuario_destino=candidatura.aluno.usuario,
    )

    messages.info(request, "Status da candidatura atualizado.")
    return redirect("listar_vagas")

# =====================================================
# NOTIFICAÇÕES E MENSAGENS
# =====================================================

@login_required
def notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario_destino=request.user).order_by("-data_envio")
    notificacoes.filter(lida=False).update(lida=True)
    return render(request, "linkif/notificacoes.html", {"notificacoes": notificacoes})


@login_required
def mensagens(request):
    recebidas = Mensagem.objects.filter(destinatario=request.user).order_by("-data_envio")
    enviadas = Mensagem.objects.filter(remetente=request.user).order_by("-data_envio")

    if request.method == "POST":
        form = MensagemForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.remetente = request.user
            msg.data_envio = timezone.now()
            msg.save()
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect("mensagens")
    else:
        form = MensagemForm()

    context = {
        "recebidas": recebidas,
        "enviadas": enviadas,
        "form": form,
    }
    return render(request, "linkif/mensagens.html", context)

# =====================================================
# PERFIS DE FORMAÇÃO
# =====================================================

def perfil_cursos(request):
    site_config = SiteConfig.objects.first()
    perfis = PerfilFormacao.objects.all()
    return render(request, "linkif/perfil_cursos.html", {
        "perfis": perfis,
        "site_config": site_config,
    })


def perfil_detalhe(request, perfil_id):
    site_config = SiteConfig.objects.first()
    perfil = get_object_or_404(PerfilFormacao, id=perfil_id)
    return render(request, "linkif/perfil_detalhe.html", {
        "perfil": perfil,
        "site_config": site_config,
    })
from django.shortcuts import render
from .models import HomeContent, Feature

def para_estudantes(request):
    home = HomeContent.objects.first()
    features = Feature.objects.filter(tipo='estudante')
    return render(request, 'linkif/para_estudantes.html', {
        'home': home,
        'features': features
    })

def para_empresas(request):
    home = HomeContent.objects.first()
    features = Feature.objects.filter(tipo='empresa')
    return render(request, 'linkif/para_empresas.html', {
        'home': home,
        'features': features
    })
# MINHAS CANDIDATURAS — sem imports no topo para evitar circularidades
@login_required
def minhas_candidaturas(request):
    aluno = request.user.aluno
    # usa related_name definido no model Candidatura: aluno.candidaturas
    candidaturas = aluno.candidaturas.all()
    return render(request, 'usuarios/minhas_candidaturas.html', {'candidaturas': candidaturas})

