import django_tables2 as tables
from usuarios.models import Usuario

class AlunoTable(tables.Table):
    foto = tables.TemplateColumn(
        """
        {% if record.foto %}
            <img src="{{ record.foto.url }}" style="width:45px;height:45px;border-radius:50%;object-fit:cover;">
        {% else %}
            <div style="width:45px;height:45px;border-radius:50%;background:#e6ecf0;display:flex;align-items:center;justify-content:center;">
                <i class="bi bi-person" style="font-size:20px;color:#6c7a89;"></i>
            </div>
        {% endif %}
        """,
        verbose_name="Foto",
        orderable=False,
    )

    portfolio = tables.TemplateColumn(
        """
        {% if record.portfolio %}
          <a href="{{ record.portfolio }}" target="_blank" class="btn btn-sm btn-outline-primary">Portfólio</a>
        {% else %}
          <span class="text-muted">—</span>
        {% endif %}
        """,
        verbose_name="Portfólio",
        orderable=False,
    )

    curriculo = tables.TemplateColumn(
        """
        {% if record.curriculo %}
          <a href="{{ record.curriculo.url }}" class="btn btn-sm btn-outline-success">Currículo</a>
        {% else %}
          <span class="text-muted">—</span>
        {% endif %}
        """,
        verbose_name="Currículo",
        orderable=False,
    )

    class Meta:
        model = Usuario
        template_name = "django_tables2/bootstrap5.html"
        fields = ("foto", "nome", "curso", "email", "portfolio", "curriculo")
        attrs = {
            "class": "table table-hover align-middle rounded-3 shadow-sm",
        }
