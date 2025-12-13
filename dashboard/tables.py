import django_tables2 as tables
from linkif.models import Candidatura, Vaga, PerfilFormacao, MensagemContato
from usuarios.models import Usuario


# ============================================================
#  CANDIDATURAS RECEBIDAS
# ============================================================

class CandidaturasRecebidasTable(tables.Table):

    aluno = tables.TemplateColumn(
        template_code="""
        <a href="{% url 'dashboard:ver_perfil_aluno' record.aluno.id %}"
           class="table-link table-aluno">
            <i class="bi bi-person-circle me-2"></i>
            {{ record.aluno.nome|default:record.aluno.email|truncatechars:10 }}
        </a>
        """,
        verbose_name="Aluno",
        orderable=True
    )

    vaga = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            {{ record.vaga.titulo|truncatechars:25 }}
        </span>
        """,
        verbose_name="Vaga",
        orderable=True
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
        <a href="{% url 'dashboard:empresa_candidatura_detalhe' record.id %}"
           class="btn-table">
            Ver detalhes
        </a>
        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Candidatura
        fields = ["aluno", "vaga", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}

#  APROVAR VAGAS

class AprovarVagasTable(tables.Table):

    titulo = tables.TemplateColumn(
        template_code="""
        <span class="table-text fw-bold">{{ record.titulo|truncatechars:22 }}</span>
        """,
        verbose_name="Título",
        orderable=True
    )

    empresa = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            {{ record.empresa.nome|default:record.empresa.email|truncatechars:18 }}
        </span>
        """,
        verbose_name="Empresa",
        orderable=True
    )

    tipo = tables.Column(verbose_name="Tipo")
    modalidade = tables.Column(verbose_name="Modalidade")

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
        <a href="#aprovar-{{ record.id }}" class="btn-table">Aprovar</a>
        <a href="#reprovar-{{ record.id }}" class="btn-delete">Reprovar</a>
        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Vaga
        fields = ["titulo", "empresa", "tipo", "modalidade", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}

#  GERENCIAR USUÁRIOS 

class UsuariosGeraisTable(tables.Table):

    # ===========================
    # COLUNA: Nome + ícone
    # ===========================
    nome = tables.TemplateColumn(
        template_code="""
        <span class="table-text ">
            <i class="bi bi-person-circle me-2"></i>
            {{ record.nome|default:record.email|truncatechars:22 }}
        </span>
        """,
        verbose_name="Usuário",
        orderable=False
    )

    # ===========================
    # TIPO (Aluno / Empresa)
    # ===========================
    tipo = tables.TemplateColumn(
        template_code="""
        {% if record.tipo == 'aluno' %}
            <span class="badge info"><i class="bi bi-mortarboard me-1"></i> Aluno</span>
        {% elif record.tipo == 'empresa' %}
            <span class="badge aprov"><i class="bi bi-building me-1"></i> Empresa</span>
        {% else %}
            <span class="badge pend">Outro</span>
        {% endif %}
        """,
        verbose_name="Tipo"
    )

    # ===========================
    # Status Aprovação
    # ===========================
    status_aprovacao = tables.TemplateColumn(
        template_code="""
        {% if record.status_aprovacao == 'aprovado' %}
            <span class="badge aprov"><i class="bi bi-check-circle"></i> Aprovado</span>

        {% elif record.status_aprovacao == 'pendente' %}
            <span class="badge pend"><i class="bi bi-hourglass-split"></i> Pendente</span>

        {% elif record.status_aprovacao == 'reprovado' %}
            <span class="badge recs"><i class="bi bi-x-circle"></i> Reprovado</span>

        {% else %}
            <span class="badge info">{{ record.status_aprovacao }}</span>
        {% endif %}
        """,
        verbose_name="Status"
    )
    aprovar = tables.TemplateColumn(
    template_code="""
    <div class="acoes-wrapper">

        <a href="#modal-aprovar-{{ record.id }}" class="btn-table">
            Aprovar
        </a>

        <a href="#modal-reprovar-{{ record.id }}" class="btn-delete">
            Reprovar
        </a>

    </div>
    """,
    verbose_name="Aprovação",
    orderable=False,
    empty_values=()
)

    
    # ===========================
    # AÇÕES (modal triggers)
    # ===========================
    acoes = tables.TemplateColumn(
    template_code="""
    <div class="acoes-wrapper-btn">

        {% if record.tipo == 'aluno' %}
            <a href="{% url 'dashboard:ver_perfil_aluno' record.id %}"
               class="btn-icon" title="Ver perfil">
                <i class="bi bi-eye"></i>
            </a>
        {% elif record.tipo == 'empresa' %}
            <a href="{% url 'dashboard:ver_perfil_empresa' record.id %}"
               class="btn-icon" title="Ver perfil">
                <i class="bi bi-eye"></i>
            </a>
        {% endif %}

        <a href="{% url 'dashboard:usuario_editar' record.id %}"
           class="btn-icon" title="Editar">
            <i class="bi bi-pencil-square"></i>
        </a>

        <a href="#excluir-{{ record.id }}"
           class="btn-icon btn-icon-danger" title="Excluir">
            <i class="bi bi-trash"></i>
        </a>

    </div>
    """,
    verbose_name="Ações",
    orderable=False,
    empty_values=()
)


    class Meta:
        model = Usuario
        fields = ["nome", "tipo", "status_aprovacao", "aprovar","acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}

# ============================================================
#  PERFIS DE FORMAÇÃO
# ============================================================

class PerfisFormacaoTable(tables.Table):

    nome = tables.TemplateColumn(
        template_code="""
        <span class='table-text'>
            <i class="bi bi-diagram-3 me-2"></i>
            {{ record.nome }}
        </span>
        """,
        verbose_name="Perfil",
        orderable=True
    )

    acoes = tables.TemplateColumn(
    template_code="""
    <div class="acoes-wrapper-btn">

        <a href="{% url 'dashboard:editar_perfil_formacao' record.id %}"
           class="btn-icon" title="Editar">
            <i class="bi bi-pencil-square"></i>
        </a>

        <a href="#excluir-perfil-{{ record.id }}"
           class="btn-icon btn-icon-danger"
           title="Excluir">
            <i class="bi bi-trash"></i>
        </a>

    </div>
    """,
    verbose_name="Ações",
    orderable=False,
    empty_values=()
)

    class Meta:
        model = PerfilFormacao
        fields = ["nome", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}


# ============================================================
#  MENSAGENS — CONTATO (ADMIN)
# ============================================================

class MensagensContatoTable(tables.Table):

    nome = tables.TemplateColumn(
        template_code="""
        <span class="table-text fw-bold">
            <i class="bi bi-person-circle me-2"></i>
            {{ record.nome|truncatechars:25 }}
        </span>
        """,
        verbose_name="Nome",
        orderable=True
    )

    email = tables.TemplateColumn(
        template_code="""
        <span class="table-text">{{ record.email|truncatechars:30 }}</span>
        """,
        verbose_name="E-mail",
        orderable=True
    )

    data_envio = tables.TemplateColumn(
        template_code="""
        <span class="table-text">{{ record.data_envio|date:"d/m/Y H:i" }}</span>
        """,
        verbose_name="Enviado em",
        orderable=True
    )

    respondido = tables.TemplateColumn(
        template_code="""
        {% if record.respondido %}
            <span class="badge aprov"><i class="bi bi-check2-circle me-1"></i> Respondido</span>
        {% else %}
            <span class="badge pend"><i class="bi bi-hourglass-split me-1"></i> Pendente</span>
        {% endif %}
        """,
        verbose_name="Status"
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
            <a href="#mensagem-{{ record.id }}" class="btn-table">Ver</a>

            {% if not record.respondido %}
                <a href="#responder-{{ record.id }}" class="btn-table btn-danger-table">
                    Responder
                </a>
            {% endif %}
        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = MensagemContato
        fields = ["nome", "email", "data_envio", "respondido", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}


# ============================================================
#  MENSAGENS — ALUNO
# ============================================================

class AlunoMensagensTable(tables.Table):

    mensagem = tables.TemplateColumn(
        template_code="""
        <span class='table-text'>{{ record.mensagem|truncatechars:40 }}</span>
        """,
        verbose_name="Mensagem"
    )

    data_envio = tables.TemplateColumn(
        template_code="""
        <span class="table-text">{{ record.data_envio|date:"d/m/Y H:i" }}</span>
        """,
        verbose_name="Data",
        orderable=True
    )

    resposta = tables.TemplateColumn(
        template_code="""
        <span class="table-text">{{ record.resposta|truncatechars:40 }}</span>
        """,
        verbose_name="Resposta"
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
            <a href="#mensagem-{{ record.id }}" class="btn-table">Ver</a>
        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = MensagemContato
        fields = ["mensagem", "data_envio", "resposta", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}


# ============================================================
#  MENSAGENS — EMPRESA
# ============================================================

class EmpresaMensagensTable(tables.Table):

    mensagem = tables.TemplateColumn(
        template_code="""
        <span class='table-text'>{{ record.mensagem|truncatechars:40 }}</span>
        """,
        verbose_name="Mensagem"
    )

    data_envio = tables.TemplateColumn(
        template_code="""
        <span class="table-text">{{ record.data_envio|date:"d/m/Y H:i" }}</span>
        """,
        verbose_name="Data"
    )

    resposta = tables.TemplateColumn(
        template_code="""
        <span class="table-text">{{ record.resposta|truncatechars:40 }}</span>
        """,
        verbose_name="Resposta"
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
            <a href="#mensagem-{{ record.id }}" class="btn-table">Ver</a>
        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = MensagemContato
        fields = ["mensagem", "data_envio", "resposta", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}
import django_tables2 as tables
from linkif.models import Vaga


class AcompanharVagasTable(tables.Table):

    titulo = tables.TemplateColumn(
        template_code="""
        <span class="table-text ">{{ record.titulo|truncatechars:30 }}</span>
        """,
        verbose_name="Título"
    )

    empresa = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            {{ record.empresa.nome|default:record.empresa.email|truncatechars:22 }}
        </span>
        """,
        verbose_name="Empresa"
    )

    curso = tables.TemplateColumn(
        template_code="""
        {% if record.curso %}
            {{ record.curso.nome }}
        {% else %}
            —
        {% endif %}
        """,
        verbose_name="Curso"
    )

    # STATUS BADGE — perfeito
    status = tables.TemplateColumn(
        template_code="""
         <div class=".badge">
        {% if record.status == "aprovada" %}
            <span class="badge aprov"><i class="bi bi-check-circle"></i> Aprovada</span>

        {% elif record.status == "pendente" %}
            <span class="badge pend"><i class="bi bi-hourglass-split"></i> Pendente</span>

        {% elif record.status == "reprovada" %}
            <span class="badge recs"><i class="bi bi-x-circle"></i> Reprovada</span>

        {% elif record.status == "encerrada" %}
            <span class="badge info"><i class="bi bi-lock"></i> Encerrada</span>

        {% else %}
            <span class="badge info">{{ record.get_status_display }}</span>
        {% endif %}
        </div>
        """,
        verbose_name="Status"
    )

    # ETAPA BADGE — perfeito
    etapa = tables.TemplateColumn(
        template_code="""
        <div class=".badge">
        {% if record.etapa == "pendente_aprovacao" %}
            <span class="badge pend"><i class="bi bi-hourglass"></i> Pendente aprovação</span>

        {% elif record.etapa == "publicada" %}
            <span class="badge aprov"><i class="bi bi-megaphone"></i> Publicada</span>

        {% elif record.etapa == "inscricoes_fechadas" %}
            <span class="badge recs"><i class="bi bi-door-closed"></i> Inscrições fechadas</span>

        {% elif record.etapa == "analise_curriculos" %}
            <span class="badge info"><i class="bi bi-search"></i> Análise de currículos</span>

        {% elif record.etapa == "entrevistas" %}
            <span class="badge info"><i class="bi bi-people"></i> Entrevistas</span>

        {% elif record.etapa == "finalizada" %}
            <span class="badge aprov"><i class="bi bi-flag"></i> Finalizada</span>

        {% else %}
            <span class="badge info">{{ record.get_etapa_display }}</span>
        {% endif %}
        </div>
        """,
        verbose_name="Etapa"
    )
    candidaturas = tables.TemplateColumn(
        template_code="""
            <span class="table-text">{{ record.candidaturas.count }}</span>
        """,
        verbose_name="Candidatos"
    )
    acoes = tables.TemplateColumn(
    template_code="""
    <div class="acoes-wrapper">

        {% if record.empresa_id == request.user.id %}
            <a href="#gerenciar-{{ record.id }}" class="btn-table">
                Gerenciar
            </a>
        {% else %}
            <span class="text-muted"</span>
        {% endif %}

    </div>
    """,
    verbose_name="Ações",
    orderable=False,
    empty_values=()
)


    class Meta:
        model = Vaga
        fields = ["titulo", "empresa", "curso", "status", "etapa","candidaturas", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}
class AcompanharVagasEmpresaTable(tables.Table):

    titulo = tables.TemplateColumn(
        template_code="""
            <span class="table-text">
                <i class="bi bi-briefcase me-2"></i>
                {{ record.titulo|truncatechars:25 }}
            </span>
        """,
        verbose_name="Título"
    )

    tipo = tables.Column(verbose_name="Tipo")
    modalidade = tables.Column(verbose_name="Modalidade")

    etapa = tables.TemplateColumn(
        template_code="""
        {% if record.etapa == "pendente_aprovacao" %}
            <span class="badge pend"><i class="bi bi-hourglass"></i> Pendente aprovação</span>
        {% elif record.etapa == "publicada" %}
            <span class="badge aprov"><i class="bi bi-megaphone"></i> Publicada</span>
        {% elif record.etapa == "inscricoes_fechadas" %}
            <span class="badge recs"><i class="bi bi-door-closed"></i> Inscrições fechadas</span>
        {% elif record.etapa == "analise_curriculos" %}
            <span class="badge info"><i class="bi bi-search"></i> Análise de currículos</span>
        {% elif record.etapa == "entrevistas" %}
            <span class="badge info"><i class="bi bi-people"></i> Entrevistas</span>
        {% elif record.etapa == "finalizada" %}
            <span class="badge aprov"><i class="bi bi-flag"></i> Finalizada</span>
        {% endif %}
        """,
        verbose_name="Etapa"
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
            <a href="#gerenciar-{{ record.id }}" class="btn-table">
                Gerenciar
            </a>
        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Vaga
        fields = ["titulo", "tipo", "modalidade", "etapa", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}
