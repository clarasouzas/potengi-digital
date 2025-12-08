# tables.py
import django_tables2 as tables
from usuarios.models import Usuario
class UsuarioTabela(tables.Table):
    estudante = tables.TemplateColumn("""
        <a href="{% url 'dashboard:ver_perfil_aluno' record.id %}" class="table-link">
            <i class="bi bi-person-fill me-2"></i>
            {{ record.first_name|default:record.email|truncatechars:20 }}
        </a>
    """, verbose_name="Estudante")

    curso = tables.TemplateColumn("""
        <span class="table-text desc">{{ record.curso|default:"—" }}</span>
    """, verbose_name="Curso")

    class Meta:
        model = Usuario
        template_name = "linkif/table.html"
        fields = ["estudante", "curso"]
        attrs = {"class": "linkif-table"}
