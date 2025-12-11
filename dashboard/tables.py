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
        <a href="{% url 'dashboard:empresa_candidatura_detalhe' record.id %}"
           class="btn-table">
            Ver detalhes
        </a>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Candidatura
        fields = ["aluno", "vaga", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}


# ============================================================
#  APROVAR ALUNOS
# ============================================================

class AprovarAlunosTable(tables.Table):

    nome = tables.TemplateColumn(
        template_code="""
        <a href="{% url 'dashboard:ver_perfil_aluno' record.id %}"
           class="table-link">
            <i class="bi bi-person-circle me-2"></i>
            {{ record.nome|default:record.email|truncatechars:30 }}
        </a>
        """,
        verbose_name="Aluno",
        orderable=True
    )

    curso = tables.Column(verbose_name="Curso")

    acoes = tables.TemplateColumn(
        template_code="""
        <a href="#aprovar-{{ record.id }}" class="btn-table">Aprovar</a>
        <a href="#rejeitar-{{ record.id }}" class="btn-delete">Rejeitar</a>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Usuario
        fields = ["nome", "curso", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}


# ============================================================
#  APROVAR EMPRESAS
# ============================================================

class AprovarEmpresasTable(tables.Table):

    nome = tables.TemplateColumn(
        template_code="""
        <a href="{% url 'dashboard:ver_perfil_empresa' record.id %}"
           class="table-link">
            <i class="bi bi-building me-2"></i>
            {{ record.nome|default:record.email|truncatechars:12 }}
        </a>
        """,
        verbose_name="Empresa",
        orderable=True
    )

    cidade = tables.Column(verbose_name="Cidade")

    acoes = tables.TemplateColumn(
        template_code="""
        <a href="#aprovar-{{ record.id }}" class="btn-table">Aprovar</a>
        <a href="#rejeitar-{{ record.id }}" class="btn-delete">Reprovar</a>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Usuario
        fields = ["nome", "cidade", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}


# ============================================================
#  APROVAR VAGAS
# ============================================================

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
        <a href="#aprovar-{{ record.id }}" class="btn-table">Aprovar</a>
        <a href="#reprovar-{{ record.id }}" class="btn-delete">Reprovar</a>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Vaga
        fields = ["titulo", "empresa", "tipo", "modalidade", "acoes"]
        template_name = "dashboard/table.html"
        attrs = {"class": "linkif-table"}


# ============================================================
#  USUÁRIOS (GERENCIAR)
# ============================================================

class UsuariosTable(tables.Table):

    nome = tables.TemplateColumn(
        template_code="""
        <a href="{% if record.tipo == 'aluno' %}{% url 'dashboard:ver_perfil_aluno' record.id %}
                 {% elif record.tipo == 'empresa' %}{% url 'dashboard:ver_perfil_empresa' record.id %}
                 {% else %}#{% endif %}"
           class="table-link">
            <i class="bi bi-person-circle me-2"></i>
            {{ record.nome|default:record.email|truncatechars:20 }}
        </a>
        """,
        verbose_name="Usuário",
        orderable=False
    )

    tipo = tables.TemplateColumn(
        template_code="""
        <span class="table-text">{{ record.get_tipo_display }}</span>
        """,
        verbose_name="Tipo"
    )

    status = tables.TemplateColumn(
        template_code="""
        {% if record.is_approved %}
            <span class="badge aprov">
                <i class="bi bi-check2-circle me-1"></i>Aprovado
            </span>
        {% else %}
            <span class="badge pend">
                <i class="bi bi-hourglass-split me-1"></i>Pendente
            </span>
        {% endif %}
        """,
        verbose_name="Status",
        orderable=False
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
            <a href="{% url 'dashboard:usuario_editar' record.id %}" class="btn-table">Editar</a>

            {% if record.id != request.user.id %}
                <a href="#excluir-{{ record.id }}" class="btn-delete">Excluir</a>
            {% endif %}
        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = Usuario
        fields = ["nome", "tipo", "status", "acoes"]
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

    competencias = tables.TemplateColumn(
        template_code="{{ record.competencia_set.count }}",
        verbose_name="Competências"
    )

    areas = tables.TemplateColumn(
        template_code="{{ record.areaatuacaoperfil_set.count }}",
        verbose_name="Áreas"
    )

    acoes = tables.TemplateColumn(
        template_code="""
        <div class="acoes-wrapper">
            <a href="{% url 'dashboard:editar_perfil_formacao' record.id %}"
               class="btn-table">Editar</a>

            <a href="{% url 'dashboard:excluir_perfil_formacao' record.id %}"
               class="btn-delete">Excluir</a>
        </div>
        """,
        verbose_name="Ações",
        orderable=False
    )

    class Meta:
        model = PerfilFormacao
        fields = ["nome", "competencias", "areas", "acoes"]
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
