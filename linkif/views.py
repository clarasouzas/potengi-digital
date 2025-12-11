from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django_tables2 import RequestConfig

from .filters import VagaFilter, AlunoFilter
from .tables import UsuarioTabela
from .models import Vaga, Candidatura, SiteConfig, PerfilFormacao
from .forms import VagaForm, CandidaturaForm, ContatoForm
from usuarios.models import Usuario
def index(request):
    site_config = SiteConfig.objects.first()
    vagas = Vaga.objects.filter(status="aprovada").order_by("-data_publicacao")[:6]
    perfis = PerfilFormacao.objects.all().order_by("ordem", "nome")

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
        "site": site_config,
        "vagas": vagas,
        "perfis": perfis,
        "form": form,
    })
@login_required
@permission_required("usuarios.can_candidatar", raise_exception=True)
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, status="aprovada")

    if not request.user.is_approved:
        messages.error(request, "Seu cadastro ainda não foi aprovado pela coordenação.")
        return redirect("linkif:para_estudantes")

    aluno = request.user

    if Candidatura.objects.filter(vaga=vaga, aluno=aluno).exists():
        messages.warning(request, "Você já se candidatou a esta vaga.")
        return redirect("linkif:para_estudantes")

    form = CandidaturaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        candidatura = form.save(commit=False)
        candidatura.vaga = vaga
        candidatura.aluno = aluno
        candidatura.status = "em_analise"
        candidatura.data_candidatura = timezone.now()
        candidatura.save()

        messages.success(request, "Candidatura enviada com sucesso!")
        return redirect("linkif:para_estudantes")

    return render(request, "linkif/candidatar.html", {
        "form": form,
        "vaga": vaga,
    })

def perfil_detalhe(request, perfil_id):
    perfil = get_object_or_404(PerfilFormacao, id=perfil_id)
    site_config = SiteConfig.objects.first()

    return render(request, "linkif/perfil_detalhe.html", {
        "perfil": perfil,
        "site_config": site_config,
    })
def para_estudantes(request):
    # agora só mostra vagas publicadas
    vagas_qs = Vaga.objects.filter(
        etapa="publicada"
    ).order_by("-data_publicacao")

    filtro = VagaFilter(request.GET, queryset=vagas_qs)
    vagas_filtradas = filtro.qs

    paginator = Paginator(vagas_filtradas, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "linkif/para_estudantes.html", {
        "vagas": page_obj,
        "filtro": filtro,
    })

def para_empresas(request):
    return render(request, "linkif/para_empresas.html")
@login_required
@permission_required("usuarios.can_explorar_alunos", raise_exception=True)
def explorar_perfis(request):
    qs = Usuario.objects.filter(tipo="aluno", is_approved=True)

    # FILTRA PELO CURSO VINDO DA URL
    curso = request.GET.get("curso")
    if curso:
        qs = qs.filter(curso__icontains=curso)

    filtro = AlunoFilter(request.GET, queryset=qs)
    table = UsuarioTabela(filtro.qs)

    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    return render(request, "linkif/explorar_tabela.html", {
        "table": table,
        "filtro": filtro,
        "curso_selecionado": curso
    })

    
@login_required
def ver_perfil_aluno(request, pk):

    aluno = get_object_or_404(Usuario, id=pk, tipo="aluno")

    if request.user.tipo not in ["empresa", "coordenador"] and request.user != aluno:
        return redirect("dashboard:inicio")

    return render(request, "dashboard/aluno/perfil_publico.html", {
        "aluno": aluno
    })
    
def vaga_detalhe(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id, status="aprovada")
    site_config = SiteConfig.objects.first()

    return render(request, "linkif/vaga_detalhe.html", {
        "vaga": vaga,
        "site_config": site_config,
    })
