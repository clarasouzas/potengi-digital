from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

from .filters import VagaFilter

from .models import (
    Vaga,
    Candidatura,
    Mensagem,
    SiteConfig,
    HomeContent,
    PerfilFormacao,
    Feature,
)

from .forms import VagaForm, CandidaturaForm, ContatoForm
from usuarios.models import Usuario   # único modelo agora


# ================================
# AUXILIARES
# ================================
def is_coordenador(user):
    return user.is_authenticated and user.tipo == "coordenador"

def is_empresa(user):
    return user.is_authenticated and user.tipo == "empresa"

def is_aluno(user):
    return user.is_authenticated and user.tipo == "aluno"


# ================================
# HOME
# ================================
def index(request):
    site = SiteConfig.objects.first()
    home = HomeContent.objects.first()
    vagas = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")[:6]

    perfis = list(PerfilFormacao.objects.all().order_by("ordem", "nome"))
    if len(perfis) > 3:
        perfis = perfis + perfis[:2]

    form = ContatoForm(request.POST or None)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "Você precisa estar logada para enviar uma mensagem.")
            return redirect("usuarios:login")

        if form.is_valid():
            form.save()
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect("linkif:index")

    return render(request, "linkif/index.html", {
        "site": site,
        "home": home,
        "vagas": vagas,
        "perfis": perfis,
        "form": form,
    })


# ================================
# LISTAR VAGAS
# ================================
def listar_vagas(request):
    vagas_qs = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")

    filtro = VagaFilter(request.GET, queryset=vagas_qs)
    vagas_filtradas = filtro.qs

    paginator = Paginator(vagas_filtradas, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "linkif/vagas.html", {
        "vagas": page_obj,
        "filtro": filtro,
    })


# ================================
# CANDIDATURA
# ================================
@login_required
@user_passes_test(is_aluno)
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, status="aprovada")

    # verificar aprovação do usuário (coordenador precisa aprovar)
    if not request.user.is_approved:
        messages.error(request, "Seu cadastro ainda não foi aprovado pela coordenação.")
        return redirect("linkif:listar_vagas")

    aluno = request.user  # agora o próprio usuário é o aluno

    # já existe candidatura
    if Candidatura.objects.filter(vaga=vaga, aluno=aluno).exists():
        messages.warning(request, "Você já se candidatou a esta vaga.")
        return redirect("linkif:listar_vagas")

    form = CandidaturaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        candidatura = form.save(commit=False)
        candidatura.vaga = vaga
        candidatura.aluno = aluno
        candidatura.status = "em_analise"
        candidatura.data_candidatura = timezone.now()
        candidatura.save()

        messages.success(request, "Candidatura enviada com sucesso!")
        return redirect("linkif:listar_vagas")

    return render(request, "linkif/candidatar.html", {
        "form": form,
        "vaga": vaga,
    })


# ================================
# PERFIS DE FORMAÇÃO
# ================================
def perfil_cursos(request):
    perfis = PerfilFormacao.objects.all()
    site_config = SiteConfig.objects.first()

    return render(request, "linkif/perfil_cursos.html", {
        "perfis": perfis,
        "site_config": site_config,
    })


def perfil_detalhe(request, perfil_id):
    perfil = get_object_or_404(PerfilFormacao, id=perfil_id)
    site_config = SiteConfig.objects.first()

    return render(request, "linkif/perfil_detalhe.html", {
        "perfil": perfil,
        "site_config": site_config,
    })


# ================================
# PÁGINAS ESTÁTICAS
# ================================
def para_estudantes(request):
    home = HomeContent.objects.first()
    features = Feature.objects.filter(tipo="estudante")

    return render(request, "linkif/para_estudantes.html", {
        "home": home,
        "features": features,
    })


def para_empresas(request):
    home = HomeContent.objects.first()
    features = Feature.objects.filter(tipo="empresa")

    return render(request, "linkif/para_empresas.html", {
        "home": home,
        "features": features,
    })


# ================================
# EXPLORAR PERFIS (Coordenação / Empresas)
# ================================
@login_required
def explorar_perfis(request):
    if request.user.tipo not in ["coordenador", "empresa"]:
        return redirect('linkif:index')

    alunos = Usuario.objects.filter(tipo="aluno", is_approved=True)

    return render(request, "linkif/explorar.html", {
        "alunos": alunos
    })
# detalhar vaga
def vaga_detalhe(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, status="aprovada")
    site_config = SiteConfig.objects.first()
    return render(request, "linkif/vaga_detalhe.html", {
        "vaga": vaga,
        "site_config": site_config,
    })
