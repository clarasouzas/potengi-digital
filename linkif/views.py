from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from usuarios.models import Aluno


from .models import (
    Vaga,
    Candidatura,
    Mensagem,
    SiteConfig,
    HomeContent,
    AreaAtuacao,
    PerfilFormacao,
    Feature,
    
)
from .forms import VagaForm, CandidaturaForm, ContatoForm
from usuarios.models import Empresa, Usuario


# ================================
# AUXILIARES
# ================================
def is_coordenador(user):
    return user.is_authenticated and getattr(user, "tipo", "") == "coordenador"

def is_empresa(user):
    return user.is_authenticated and getattr(user, "tipo", "") == "empresa"

def is_aluno(user):
    return user.is_authenticated and getattr(user, "tipo", "") == "aluno"


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

    # envio de mensagem
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
# LISTAGEM DE VAGAS PÚBLICAS
# ================================
def listar_vagas(request):
    vagas = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")
    areas = AreaAtuacao.objects.all()

    filtros = {
        "titulo": request.GET.get("titulo"),
        "area": request.GET.get("area"),
        "cidade": request.GET.get("cidade"),
        "tipo": request.GET.get("tipo"),
    }

    if filtros["titulo"]:
        vagas = vagas.filter(titulo__icontains=filtros["titulo"])
    if filtros["area"]:
        vagas = vagas.filter(area__nome__icontains=filtros["area"])
    if filtros["cidade"]:
        vagas = vagas.filter(cidade__icontains=filtros["cidade"])
    if filtros["tipo"]:
        vagas = vagas.filter(tipo__iexact=filtros["tipo"])

    return render(request, "linkif/vagas.html", {"vagas": vagas, "areas": areas})


# ================================
# CANDIDATURA
# ================================
@login_required
@user_passes_test(is_aluno)
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, status="aprovada")

    aluno = request.user.aluno
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
@login_required
def explorar_perfis(request):
    if request.user.tipo not in ["coordenador", "empresa"]:
        return redirect('linkif:index')  # ou homepage

    alunos = Aluno.objects.all()
    return render(request, "linkif/explorar.html", {"alunos": alunos})



