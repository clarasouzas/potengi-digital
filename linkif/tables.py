import django_tables2 as tables
from usuarios.models import Usuario


class UsuarioTabela(tables.Table):
    class Meta:
        model = Usuario
        template_name = "django_tables2/bootstrap5.html"

        fields = [
            "foto",
            "nome",
            "email",
            "tipo",
            "curso",
            "portfolio",
            "curriculo",
        ]

        attrs = {
            "class": "table table-hover align-middle shadow-sm usuario-table",
        }
