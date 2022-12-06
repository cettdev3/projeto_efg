from django_filters import FilterSet, AllValuesFilter, ModelChoiceFilter
from appprojeto1.models import Metas_efg, Metas_escolas, Cadastrar_curso


class AprovarCursosFilter(FilterSet):
    ano = AllValuesFilter()
    escola = ModelChoiceFilter(queryset=Metas_escolas.objects.filter(tipo=0))
    curso = ModelChoiceFilter(queryset=Cadastrar_curso.objects.all())
    trimestre = AllValuesFilter()

    class Meta:
        model = Metas_efg

        exclude = (
            'id',
            'num_edital',
        )
