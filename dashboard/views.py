# dashboard/views.py
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import (
    login_required,
    permission_required
)
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

from django_tables2 import RequestConfig

from linkif.models import (
    PerfilFormacao,
    Competencia,
    AreaAtuacaoPerfil,
    Vaga,
    Candidatura,
    SiteConfig,
    MensagemContato
)

from linkif.forms import (
    PerfilFormacaoForm,
    CompetenciaForm,
    AreaAtuacaoForm,
    VagaForm,
    SiteConfigForm,
    ContatoForm
)

from usuarios.models import Usuario
from usuarios.forms import (
    AlunoEditForm,
    EmpresaEditForm,
    CoordenadorEditForm,
    UsuarioEditFormSimples
)

from dashboard.tables import (
    CandidaturasRecebidasTable,
    AprovarAlunosTable,
    AprovarEmpresasTable,
    AprovarVagasTable,
    UsuariosTable,
    PerfisFormacaoTable,
    MensagensContatoTable,
    AlunoMensagensTable,
    EmpresaMensagensTable,
    AcompanharVagasTable,
    AcompanharVagasEmpresaTable
)

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
                return redirect("dashboard:empresa_painel")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@login_required
def inicio(request):
    if request.user.tipo == "aluno":
        return redirect("dashboard:aluno_painel")
    if request.user.tipo == "empresa":
        return redirect("dashboard:empresa_painel")
    return redirect("dashboard:coordenacao_painel")

# Aluno 

@login_required
@permission_required("usuarios.acesso_aluno", raise_exception=True)
def aluno_painel(request):

    vagas = (
        Vaga.objects
        .filter(status="aprovada")
        .order_by("-data_publicacao")[:6]
    )

    candidaturas_ativas = (
        Candidatura.objects
        .filter(aluno=request.user)
        .exclude(status="recusado")
    )

    candidaturas_ultimas = (
        Candidatura.objects
        .filter(aluno=request.user)
        .order_by("-data_candidatura")[:5]
    )
    if request.user.curso:
        recomendadas = Vaga.objects.filter(
            status="aprovada",
            curso__nome=request.user.curso
        )[:3]
    else:
        recomendadas = Vaga.objects.none()



    return render(request, "dashboard/aluno/painel.html", {
        "vagas": vagas,
        "candidaturas_ativas": candidaturas_ativas,
        "candidaturas_ultimas": candidaturas_ultimas,
        "recomendadas": recomendadas,
    })
    
@login_required
@permission_required("usuarios.acesso_aluno", raise_exception=True)
@permission_required("usuarios.aluno_aprovado", raise_exception=True)
@requer_aprovacao("aluno")
def aluno_candidaturas(request):

    lista = (
        Candidatura.objects
        .filter(aluno=request.user)
        .order_by('-data_candidatura')
    )

    paginator = Paginator(lista, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "dashboard/aluno/candidaturas.html", {
        "candidaturas": page_obj,
        "page_obj": page_obj
    })
    
@login_required
@permission_required("usuarios.acesso_aluno", raise_exception=True)
@permission_required("usuarios.aluno_aprovado", raise_exception=True)
@requer_aprovacao("aluno")
def cancelar_candidatura(request, cand_id):

    candidatura = get_object_or_404(
        Candidatura, id=cand_id, aluno=request.user
    )

    if request.method == "POST":
        candidatura.delete()
        messages.success(request, "Candidatura cancelada com sucesso.")
        return redirect("dashboard:aluno_candidaturas")

    return render(
        request,
        "dashboard/aluno/cancelar_candidatura.html",
        {"candidatura": candidatura}
    )
def aluno_mensagens(request):
    msgs = MensagemContato.objects.filter(
        email=request.user.email,
        respondido=True
    ).order_by('-data_envio')

    table = AlunoMensagensTable(msgs)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    form = ContatoForm(initial={"nome": request.user.username , "email": request.user.email})

    return render(request, "dashboard/aluno/mensagens.html", {
        "table": table,
        "form": form,
    })

def enviar_mensagem(request):
    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensagem enviada com sucesso!")
    return redirect("dashboard:aluno_mensagens")

# Empresa

@login_required
@permission_required("usuarios.acesso_empresa", raise_exception=True)
def empresa_painel(request):
    usuario = request.user

    vagas = Vaga.objects.filter(empresa=usuario)
    vagas_recentes = vagas.order_by("-id")[:4]

    total_vagas = vagas.count()
    vagas_pendentes = vagas.filter(status="pendente").count()
    total_candidaturas = (
        Candidatura.objects.filter(vaga__empresa=usuario).count()
    )

    context = {
        "total_vagas": total_vagas,
        "vagas_pendentes": vagas_pendentes,
        "total_candidaturas": total_candidaturas,
        "vagas_recentes": vagas_recentes,
    }

    return render(request, "dashboard/empresa/painel.html", context)
def empresa_mensagens(request):
    msgs = MensagemContato.objects.filter(
        email=request.user.email,
        respondido=True
    ).order_by('-data_envio')

    table = EmpresaMensagensTable(msgs)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    form = ContatoForm(initial={"nome": request.user.username , "email": request.user.email})

    return render(request, "dashboard/empresa/mensagens.html", {
        "table": table,
        "form": form,
    })
@login_required
@permission_required("usuarios.acesso_empresa", raise_exception=True)
@permission_required("usuarios.empresa_aprovada", raise_exception=True)
@requer_aprovacao("empresa")
def empresa_vagas(request):

    vagas = (
        Vaga.objects
        .filter(empresa=request.user)
        .order_by("-id")
    )

    return render(request, "dashboard/empresa/minhas_vagas.html", {
        "vagas": vagas,
    })
    
@login_required
@permission_required("usuarios.can_post_vaga", raise_exception=True)
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
@permission_required("usuarios.acesso_empresa", raise_exception=True)
@permission_required("usuarios.empresa_aprovada", raise_exception=True)
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
@permission_required("usuarios.acesso_empresa", raise_exception=True)
@permission_required("usuarios.empresa_aprovada", raise_exception=True)
@requer_aprovacao("empresa")
def empresa_excluir_vaga(request, vaga_id):

    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)

    if request.method == "POST":
        vaga.delete()
        messages.error(request, "Vaga excluída com sucesso.")
        return redirect("dashboard:empresa_vagas")

    return render(request, "dashboard/empresa/confirmar_exclusao.html", {
        "vaga": vaga,
    })
    
@login_required
@permission_required("usuarios.acesso_empresa", raise_exception=True)
@permission_required("usuarios.empresa_aprovada", raise_exception=True)
@requer_aprovacao("empresa")
def empresa_candidaturas(request):

    candidaturas = Candidatura.objects.filter(vaga__empresa=request.user)

    table = CandidaturasRecebidasTable(candidaturas)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    return render(request, "dashboard/empresa/candidaturas_tabela.html", {
        "table": table
    })
    
@login_required
@permission_required("usuarios.acesso_empresa", raise_exception=True)
@permission_required("usuarios.empresa_aprovada", raise_exception=True)
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

@login_required
def ver_perfil_aluno(request, pk):

    aluno = get_object_or_404(Usuario, id=pk, tipo="aluno")

    if request.user.tipo not in ["empresa", "coordenador"] and request.user != aluno:
        return redirect("dashboard:inicio")

    return render(request, "dashboard/aluno/perfil_publico.html", {
        "aluno": aluno
    })
    
@login_required
def ver_perfil_empresa(request, pk):
    empresa = get_object_or_404(Usuario, pk=pk, tipo="empresa")
    return render(request, "dashboard/empresa/perfil_empresa.html", {"empresa": empresa})


@login_required
@permission_required("usuarios.acesso_empresa", raise_exception=True)
def empresa_acompanhar_vagas(request):

    # empresa só gerencia vagas aprovadas/publicadas
    vagas = Vaga.objects.filter(
        empresa=request.user,
        status="aprovada"  # só aparece quando coordenação aprova
    ).order_by("-data_publicacao")

    table = AcompanharVagasEmpresaTable(vagas)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    etapa_choices = Vaga.ETAPA_CHOICES

    return render(request, "dashboard/empresa/acompanhar_vagas.html", {
        "table": table,
        "etapa_choices": etapa_choices,
    })
@login_required
@permission_required("usuarios.acesso_empresa", raise_exception=True)
def empresa_atualizar_etapa(request, vaga_id):

    vaga = get_object_or_404(
        Vaga,
        id=vaga_id,
        empresa=request.user,
        status="aprovada"  # impedir mexer em vagas pendentes
    )

    if request.method == "POST":
        nova = request.POST.get("nova_etapa")
        if nova in dict(Vaga.ETAPA_CHOICES):
            vaga.etapa = nova
            vaga.save()
            messages.success(request, "Etapa atualizada com sucesso!")
        else:
            messages.error(request, "Etapa inválida.")

    return redirect("dashboard:empresa_acompanhar_vagas")

@login_required
def atualizar_etapa_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    user = request.user

    # COORDENAÇÃO pode atualizar sempre
    if user.tipo == "coordenador":
        pode_editar = True

    # EMPRESA só pode editar se a vaga estiver aprovada / publicada
    elif user.tipo == "empresa":
        pode_editar = vaga.status == "aprovada"
    else:
        pode_editar = False

    if not pode_editar:
        messages.error(request, "Você não tem permissão para alterar a etapa desta vaga.")
        return redirect("dashboard:empresa_vagas")

    # processa alteração
    nova_etapa = request.POST.get("nova_etapa")
    if nova_etapa not in dict(Vaga.ETAPA_CHOICES):
        messages.error(request, "Etapa inválida.")
        return redirect("dashboard:empresa_vagas")

    vaga.etapa = nova_etapa

    # se for publicada pela coordenação → também marca como aprovada
    if nova_etapa == "publicada" and user.tipo == "coordenador":
        vaga.status = "aprovada"
        vaga.data_publicacao = timezone.now()

    vaga.save()

    messages.success(request, "Etapa da vaga atualizada com sucesso.")
    return redirect(request.META.get("HTTP_REFERER", "dashboard:empresa_vagas"))
# Coordenação 

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
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

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def aprovar_alunos(request):

    alunos = Usuario.objects.filter(tipo="aluno", is_approved=False)

    table = AprovarAlunosTable(alunos)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    return render(request, "dashboard/coordenacao/aprovar_alunos.html", {
        "table": table,
        "total": alunos.count(),
    })

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def aprovar_aluno_action(request, user_id):
    aluno = get_object_or_404(Usuario, id=user_id, tipo="aluno")
    aluno.is_approved = True
    aluno.save()
    messages.success(request, "Aluno aprovado com sucesso.")
    return redirect("dashboard:aprovar_alunos")
 
@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def reprovar_aluno_action(request, user_id):

    aluno = get_object_or_404(Usuario, id=user_id, tipo="aluno")
    aluno.delete()

    messages.error(request, "Aluno reprovado e removido do sistema.")
    return redirect("dashboard:aprovar_alunos")

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def aprovar_empresas(request):

    empresas = Usuario.objects.filter(tipo="empresa", is_approved=False)

    table = AprovarEmpresasTable(empresas)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    return render(request, "dashboard/coordenacao/aprovar_empresas.html", {
        "table": table,
        "total": empresas.count(),
    })

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def aprovar_empresa_action(request, user_id):

    empresa = get_object_or_404(Usuario, id=user_id, tipo="empresa")

    empresa.is_approved = True
    empresa.save()

    messages.success(request, "Empresa aprovada com sucesso!")
    return redirect("dashboard:aprovar_empresas")

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def reprovar_empresa_action(request, user_id):

    empresa = get_object_or_404(Usuario, id=user_id, tipo="empresa")
    empresa.delete()

    messages.error(request, "Empresa rejeitada e removida.")
    return redirect("dashboard:aprovar_empresas")

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def aprovar_vagas(request):

    vagas = Vaga.objects.filter(status="pendente")

    table = AprovarVagasTable(vagas)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    return render(request, "dashboard/coordenacao/aprovar_vagas.html", {
        "table": table,
        "total": vagas.count(),
    })


    
@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def aprovar_vaga_action(request, vaga_id):

    vaga = get_object_or_404(Vaga, id=vaga_id)

    # muda status
    vaga.status = "aprovada"

    # muda etapa automaticamente
    vaga.etapa = "publicada"

    # registra aprovado por + data
    vaga.aprovado_por = request.user
    vaga.data_publicacao = timezone.now()

    vaga.save()

    messages.success(request, "Vaga aprovada e publicada com sucesso!")
    return redirect("dashboard:aprovar_vagas")


@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def reprovar_vaga_action(request, vaga_id):

    vaga = get_object_or_404(Vaga, id=vaga_id)

    vaga.status = "reprovada"
    vaga.etapa = "rascunho"

    vaga.save()

    messages.warning(request, "Vaga reprovada.")
    return redirect("dashboard:aprovar_vagas")



@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def acompanhar_vagas(request):

    qs = Vaga.objects.all().order_by('-data_publicacao', '-id')

    table = AcompanharVagasTable(qs)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    return render(request, "dashboard/coordenacao/acompanhar_vagas.html", {
        "table": table,
        "etapa_choices": Vaga.ETAPA_CHOICES,
    })

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def atualizar_etapa_vaga(request, vaga_id):

    vaga = get_object_or_404(Vaga, id=vaga_id)

    if request.method == "POST":
        nova = request.POST.get("nova_etapa")

        if nova not in dict(Vaga.ETAPA_CHOICES):
            messages.error(request, "Etapa inválida.")
            return redirect("dashboard:acompanhar_vagas")

        vaga.etapa = nova

        # automático: coordenação mudou → já publica
        if nova == "publicada":
            vaga.status = "aprovada"
            if not vaga.data_publicacao:
                vaga.data_publicacao = timezone.now()

        vaga.save()
        messages.success(request, "Etapa atualizada com sucesso.")

    return redirect("dashboard:acompanhar_vagas")
@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def coordenacao_empresas(request):

    empresas = Usuario.objects.filter(tipo="empresa").order_by("-id")

    return render(request, "dashboard/coordenacao/empresas_list.html", {
        "empresas": empresas
    })
    
@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
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
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def coordenacao_empresa_excluir(request, empresa_id):

    empresa = get_object_or_404(Usuario, id=empresa_id, tipo="empresa")

    empresa.delete()
    messages.success(request, "Empresa removida com sucesso.")

    return redirect("dashboard:empresas")
@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def coordenacao_usuarios(request):

    usuarios = Usuario.objects.all().order_by("tipo", "username")

    table = UsuariosTable(usuarios)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    return render(request, "dashboard/coordenacao/usuarios_list.html", {
        "table": table,
        "total": usuarios.count(),

    })

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
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
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def coordenacao_usuario_excluir(request, user_id):

    usuario = get_object_or_404(Usuario, id=user_id)

    usuario.delete()

    messages.error(request, "Usuário excluído com sucesso.")
    return redirect("dashboard:usuarios")

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
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

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def listar_perfis(request):

    perfis = PerfilFormacao.objects.all()

    table = PerfisFormacaoTable(perfis)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    return render(request, "dashboard/coordenacao/perfis_lista.html", {
        "table": table,
        "total": perfis.count(),
    })

    
@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def editar_perfil_formacao(request, pk=None):

    perfil = get_object_or_404(PerfilFormacao, pk=pk) if pk else None

    if request.method == "POST":
        form = PerfilFormacaoForm(request.POST, request.FILES, instance=perfil)

        if form.is_valid():
            perfil = form.save()
            messages.success(request, "Perfil salvo com sucesso!")
            return redirect("dashboard:editar_perfil_formacao", pk=perfil.pk)

        messages.error(request, "Corrija os erros no formulário.")

    else:
        form = PerfilFormacaoForm(instance=perfil)

    return render(request, "dashboard/coordenacao/perfil_form.html", {
        "form": form,
        "perfil": perfil,
        "competencias": perfil.competencias.all() if perfil else [],
        "areas": perfil.areas.all() if perfil else [],
    })
    
@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def excluir_perfil_formacao(request, pk):

    perfil = get_object_or_404(PerfilFormacao, pk=pk)
    perfil.delete()

    messages.error(request, "Perfil removido com sucesso.")
    return redirect("dashboard:listar_perfis")

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def adicionar_competencia(request, perfil_id):

    perfil = get_object_or_404(PerfilFormacao, pk=perfil_id)

    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()

        if not texto:
            messages.error(request, "A competência não pode estar vazia.")
            return redirect("dashboard:editar_perfil_formacao", pk=perfil_id)

        if perfil.competencias.filter(texto__iexact=texto).exists():
            messages.warning(request, "Esta competência já está cadastrada.")
            return redirect("dashboard:editar_perfil_formacao", pk=perfil_id)

        Competencia.objects.create(perfil=perfil, texto=texto)
        messages.success(request, "Competência adicionada com sucesso!")

    return redirect("dashboard:editar_perfil_formacao", pk=perfil_id) 

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def remover_competencia(request, pk):

    competencia = get_object_or_404(Competencia, pk=pk)
    perfil_id = competencia.perfil.id

    competencia.delete()
    messages.error(request, "Competência removida.")

    return redirect("dashboard:editar_perfil_formacao", pk=perfil_id)

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def adicionar_area(request, perfil_id):

    perfil = get_object_or_404(PerfilFormacao, pk=perfil_id)

    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        descricao = request.POST.get("descricao", "").strip()

        if not titulo:
            messages.error(request, "A área deve ter um título.")
            return redirect("dashboard:editar_perfil_formacao", pk=perfil_id)

        AreaAtuacaoPerfil.objects.create(
            perfil=perfil,
            titulo=titulo,
            descricao=descricao
        )

        messages.success(request, "Área adicionada!")

    return redirect("dashboard:editar_perfil_formacao", pk=perfil_id)

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def remover_area(request, pk):

    area = get_object_or_404(AreaAtuacaoPerfil, pk=pk)
    perfil_id = area.perfil.id

    area.delete()
    messages.error(request, "Área removida.")

    return redirect("dashboard:editar_perfil_formacao", pk=perfil_id)

# Relatórios

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def relatorios(request):

    total_usuarios = Usuario.objects.count()
    total_alunos = Usuario.objects.filter(tipo="aluno").count()
    total_empresas = Usuario.objects.filter(tipo="empresa").count()

    vagas_pendentes = Vaga.objects.filter(status="pendente").count()
    vagas_aprovadas = Vaga.objects.filter(status="aprovada").count()
    vagas_reprovadas = Vaga.objects.filter(status="reprovada").count()

    candidaturas_total = Candidatura.objects.count()
    candidaturas_aprovadas = Candidatura.objects.filter(status="aprovado").count()
    candidaturas_recusadas = Candidatura.objects.filter(status="recusado").count()
    candidaturas_pendentes = Candidatura.objects.filter(status="pendente").count()

    return render(request, "dashboard/coordenacao/relatorios.html", {
        "total_usuarios": total_usuarios,
        "total_alunos": total_alunos,
        "total_empresas": total_empresas,

        "vagas_pendentes": vagas_pendentes,
        "vagas_aprovadas": vagas_aprovadas,
        "vagas_reprovadas": vagas_reprovadas,

        "candidaturas_total": candidaturas_total,
        "candidaturas_aprovadas": candidaturas_aprovadas,
        "candidaturas_recusadas": candidaturas_recusadas,
        "candidaturas_pendentes": candidaturas_pendentes,
    })
    
# Config do Site

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def site_config(request):

    config = SiteConfig.objects.first()

    if request.method == "POST":
        form = SiteConfigForm(request.POST, request.FILES, instance=config)

        if form.is_valid():
            form.save()
            messages.success(request, "Configurações atualizadas com sucesso!")
            return redirect("dashboard:site_config")

    else:
        form = SiteConfigForm(instance=config)

    return render(request, "dashboard/coordenacao/site_config.html", {
        "form": form,
        "config": config
    })
    
@login_required
def meu_perfil(request):
    user = request.user

    foto = user.foto.url if hasattr(user, "foto") and user.foto else None

    icone = "bi bi-person-circle"

    return render(request, "dashboard/meu_perfil.html", {
        "perfil": user,
        "foto": foto,
        "icone": icone,
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
@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def mensagens_contato(request):
    mensagens = MensagemContato.objects.all()

    table = MensagensContatoTable(mensagens)
    RequestConfig(request, paginate={"per_page": 12}).configure(table)

    return render(request, "dashboard/coordenacao/mensagens_contato.html", {
        "table": table,
    })
def responder_mensagem(request, pk):
    msg = get_object_or_404(MensagemContato, id=pk)

    if request.method == "POST":
        resposta = request.POST.get("resposta")

        msg.respondido = True
        msg.resposta = resposta
        msg.save()

        messages.success(request, "Resposta enviada com sucesso!")
        return redirect("dashboard:mensagens_contato")

    return redirect("dashboard:mensagens_contato")