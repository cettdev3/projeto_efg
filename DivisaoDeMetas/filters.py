from django_filters import FilterSet, AllValuesFilter, ModelChoiceFilter
from DivisaoDeMetas.models import DivisaoDeMetasPorEscola, Escola


class DivisaoDeMetasFilter(FilterSet):
    ano = AllValuesFilter()
    escola = ModelChoiceFilter(queryset=Escola.objects.filter(tipo=0))
    
    class Meta:
        model = DivisaoDeMetasPorEscola
        
        exclude = (
            'id',
            'created_at',
            'updated_at',
        )
