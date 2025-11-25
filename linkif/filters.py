import django_filters
from .models import Vaga

class VagaFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(
        field_name='titulo',
        lookup_expr='icontains',
        label='Busque pelo nome da vaga'
    )
    cidade = django_filters.CharFilter(
        field_name='cidade',
        lookup_expr='icontains',
        label='Cidade'
    )
    tipo = django_filters.ChoiceFilter(
        field_name='tipo',
        choices=Vaga.TIPO_CHOICES,
        label='Tipo de Vaga'
    )

    class Meta:
        model = Vaga
        fields = ['titulo', 'cidade', 'tipo']
