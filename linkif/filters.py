import django_filters
from .models import Vaga, PerfilFormacao
from usuarios.models import Usuario


class VagaFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(
        field_name="titulo",
        lookup_expr="icontains",
        label="Nome da vaga",
        widget=django_filters.widgets.forms.TextInput(
            attrs={"placeholder": "Pesquisar vaga..."}
        ),
    )

    cidade = django_filters.CharFilter(
        field_name="cidade",
        lookup_expr="icontains",
        label="Cidade",
        widget=django_filters.widgets.forms.TextInput(
            attrs={"placeholder": "Ex: São Paulo do Potengi"}
        ),
    )

    tipo = django_filters.ChoiceFilter(
        field_name="tipo",
        choices=Vaga.TIPO_CHOICES,
        label="Tipo",
        empty_label="Todos os tipos",
    )

    curso = django_filters.ModelChoiceFilter(
        field_name="curso",
        queryset=PerfilFormacao.objects.none(),  # resolvido no __init__
        label="Curso",
        empty_label="Todos os cursos",
    )

    modalidade = django_filters.ChoiceFilter(
        field_name="modalidade",
        choices=Vaga.MODALIDADE_CHOICES,
        label="Modalidade",
        empty_label="Todas",
    )

    class Meta:
        model = Vaga
        fields = ["titulo", "cidade", "tipo", "curso", "modalidade"]

    # ============================
    # RESOLVE queryset dinâmico
    # ============================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters["curso"].queryset = PerfilFormacao.objects.all()

class AlunoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label="Nome")
    curso = django_filters.CharFilter(lookup_expr='icontains', label="Curso")

    class Meta:
        model = Usuario
        fields = ["nome", "curso"]
