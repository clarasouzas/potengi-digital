import django_tables2 as tables

from linkif.models import (
    Candidatura,
    Vaga,
    PerfilFormacao,
    MensagemContato,
)
from usuarios.models import Usuario


# ============================================================
# BASE TABLE (remove repetição de Meta)
# ============================================================

class BaseLinkIFTable(tables.Table):
    class Meta:
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}


# ============================================================
# CANDIDATURAS RECEBIDAS
# ============================================================

class CandidaturasRecebidasTable(BaseLinkIFTable):

    aluno = tables.TemplateColumn(
        template_code="""
        <a href="{% url 'dashboard:ver_perfil_aluno' record.aluno.id %}"
           class="table-link table-aluno">
            <i class="bi bi-person-circle me-2"></i>
            {{ record.aluno.nome|default:record.aluno.email|truncatechars:12 }}
        </a>
        """,
        verbose_name="Aluno",
        orderable=True,
    )

    vaga = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            {{ record.vaga.titulo|truncatechars:25 }}
        </span>
        """,
        verbose_name="Vaga",
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
        orderable=False,
    )

    class Meta(BaseLinkIFTable.Meta):
        model = Candidatura
        fields = ["aluno", "vaga", "acoes"]


# ============================================================
# APROVAR VAGAS (COORDENAÇÃO)
# ============================================================

class AprovarVagasTable(BaseLinkIFTable):

    titulo = tables.TemplateColumn(
        template_code="""
        <span class="table-text fw-bold">
            {{ record.titulo|truncatechars:22 }}
        </span>
        """,
        verbose_name="Título",
    )

    empresa = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            {{ record.empresa.nome|default:record.empresa.email|truncatechars:18 }}
        </span>
        """,
        verbose_name="Empresa",
    )

    tipo = tables.Column(verbose_name="Tipo")
    modalidade = tables.Column(verbose_name="Modalidade")

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">

            <a href="#"
               class="btn-table"
               data-ajax-url="{% url 'dashboard:ajax_aprovar_vaga' record.id %}"
               data-modal="modal-gerenciar">
                Aprovar
            </a>

            <a href="#"
               class="btn-delete"
               data-ajax-url="{% url 'dashboard:ajax_reprovar_vaga' record.id %}"
               data-modal="modal-gerenciar">
                Reprovar
            </a>

        </div>
        """,
        verbose_name="Ações",
        orderable=False,
    )

    class Meta(BaseLinkIFTable.Meta):
        model = Vaga
        fields = ["titulo", "empresa", "tipo", "modalidade", "acoes"]


# ============================================================
# USUÁRIOS (GERAL – COORDENAÇÃO)
# ============================================================

class UsuariosGeraisTable(BaseLinkIFTable):

    nome = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            <i class="bi bi-person-circle me-2"></i>
            {{ record.nome|default:record.email|truncatechars:22 }}
        </span>
        """,
        verbose_name="Usuário",
    )

    tipo = tables.TemplateColumn(
        template_code="""
        {% if record.tipo == 'aluno' %}
            <span class="badge info">
                <i class="bi bi-mortarboard me-1"></i> Aluno
            </span>
        {% elif record.tipo == 'empresa' %}
            <span class="badge aprov">
                <i class="bi bi-building me-1"></i> Empresa
            </span>
        {% else %}
            <span class="badge pend">Outro</span>
        {% endif %}
        """,
        verbose_name="Tipo",
    )

    status_aprovacao = tables.TemplateColumn(
        template_code="""
        {% if record.status_aprovacao == 'aprovado' %}
            <span class="badge aprov">
                <i class="bi bi-check-circle"></i> Aprovado
            </span>
        {% elif record.status_aprovacao == 'pendente' %}
            <span class="badge pend">
                <i class="bi bi-hourglass-split"></i> Pendente
            </span>
        {% elif record.status_aprovacao == 'reprovado' %}
            <span class="badge recs">
                <i class="bi bi-x-circle"></i> Reprovado
            </span>
        {% endif %}
        """,
        verbose_name="Status",
    )

    aprovacao = tables.TemplateColumn(
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
    )

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
               class="btn-icon btn-icon-danger"
               title="Excluir">
                <i class="bi bi-trash"></i>
            </a>

        </div>
        """,
        verbose_name="Ações",
        orderable=False,
    )

    class Meta(BaseLinkIFTable.Meta):
        model = Usuario
        fields = ["nome", "tipo", "status_aprovacao", "aprovacao", "acoes"]


# ============================================================
# PERFIS DE FORMAÇÃO
# ============================================================

class PerfisFormacaoTable(BaseLinkIFTable):

    nome = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            <i class="bi bi-diagram-3 me-2"></i>
            {{ record.nome }}
        </span>
        """,
        verbose_name="Perfil",
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
    )

    class Meta(BaseLinkIFTable.Meta):
        model = PerfilFormacao
        fields = ["nome", "acoes"]


# ============================================================
# MENSAGENS — CONTATO (ADMIN)
# ============================================================

class MensagensContatoTable(BaseLinkIFTable):

    nome = tables.TemplateColumn(
        template_code="""
        <span class="table-text fw-bold">
            <i class="bi bi-person-circle me-2"></i>
            {{ record.nome|truncatechars:25 }}
        </span>
        """,
        verbose_name="Nome",
    )

    email = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            {{ record.email|truncatechars:30 }}
        </span>
        """,
        verbose_name="E-mail",
    )

    data_envio = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            {{ record.data_envio|date:"d/m/Y H:i" }}
        </span>
        """,
        verbose_name="Enviado em",
    )

    respondido = tables.TemplateColumn(
        template_code="""
        {% if record.respondido %}
            <span class="badge aprov">
                <i class="bi bi-check2-circle me-1"></i> Respondido
            </span>
        {% else %}
            <span class="badge pend">
                <i class="bi bi-hourglass-split me-1"></i> Pendente
            </span>
        {% endif %}
        """,
        verbose_name="Status",
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
            <a href="#mensagem-{{ record.id }}" class="btn-table">
                Ver
            </a>

            {% if not record.respondido %}
                <a href="#responder-{{ record.id }}"
                   class="btn-table btn-danger-table">
                    Responder
                </a>
            {% endif %}
        </div>
        """,
        verbose_name="Ações",
        orderable=False,
    )

    class Meta(BaseLinkIFTable.Meta):
        model = MensagemContato
        fields = ["nome", "email", "data_envio", "respondido", "acoes"]
class AcompanharVagasTable(tables.Table):

    titulo = tables.TemplateColumn(
        template_code="""
        <span class="table-text">
            <i class="bi bi-briefcase me-2"></i>
            {{ record.titulo|truncatechars:30 }}
        </span>
        """,
        verbose_name="Título"
    )
    
    tipo = tables.Column(verbose_name="Tipo")

    status = tables.TemplateColumn(
        template_code="""
        {% if record.status == "aprovada" %}
            <span class="badge aprov"><i class="bi bi-check-circle"></i> Aprovada</span>
        {% elif record.status == "pendente" %}
            <span class="badge pend"><i class="bi bi-hourglass-split"></i> Pendente</span>
        {% elif record.status == "reprovada" %}
            <span class="badge recs"><i class="bi bi-x-circle"></i> Reprovada</span>
        {% elif record.status == "encerrada" %}
            <span class="badge info"><i class="bi bi-lock"></i> Encerrada</span>
        {% endif %}
        """,
        verbose_name="Status"
    )

    etapa = tables.TemplateColumn(
        template_code="""
        {% if record.etapa == "pendente_aprovacao" %}
            <span class="badge pend"><i class="bi bi-hourglass"></i> Pendente aprovação</span>
        {% elif record.etapa == "publicada" %}
            <span class="badge aprov"><i class="bi bi-megaphone"></i> Publicada</span>
        {% elif record.etapa == "inscricoes_fechadas" %}
            <span class="badge recs"><i class="bi bi-door-closed"></i> Inscrições fechadas</span>
        {% elif record.etapa == "analise_curriculos" %}
            <span class="badge info"><i class="bi bi-search"></i> Análise</span>
        {% elif record.etapa == "entrevistas" %}
            <span class="badge info"><i class="bi bi-people"></i> Entrevistas</span>
        {% elif record.etapa == "finalizada" %}
            <span class="badge aprov"><i class="bi bi-flag"></i> Finalizada</span>
        {% endif %}
        """,
        verbose_name="Etapa"
    )

    candidaturas = tables.TemplateColumn(
        template_code="""
        {% if perms.usuarios.acesso_coordenacao %}
            {{ record.candidaturas.count }}
        {% else %}
            —
        {% endif %}
        """,
        verbose_name="Candidatos"
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">

            {% if record.empresa_id == request.user.id or perms.usuarios.acesso_coordenacao %}
                <a href="#gerenciar-{{ record.id }}" class="btn-table">
                    Gerenciar
                </a>
            {% else %}
                <span class="text-muted">—</span>
            {% endif %}

        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Vaga
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}
        fields = [
            "titulo",
            "tipo",
            "status",
            "etapa",
            "candidaturas",
            "acoes",
        ]
