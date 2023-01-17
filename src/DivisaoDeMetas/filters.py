from django_filters import FilterSet, AllValuesFilter, ModelChoiceFilter
from DivisaoDeMetas.models import DivisaoDeMetasPorEscola, Metas_escolas


class DivisaoDeMetasFilter(FilterSet):
    ano = AllValuesFilter()
    escola = ModelChoiceFilter(queryset=Metas_escolas.objects.filter(tipo=0))
    
    class Meta:
        model = DivisaoDeMetasPorEscola
        
        exclude = (
            'id',
            'created_at',
            'updated_at',
        )
