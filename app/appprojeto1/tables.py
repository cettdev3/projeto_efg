import django_tables2 as tables
from appprojeto1.models import Metas_efg
from appprojeto1.widgets import MaterializeCssCheckboxColumn

class AprovarCursosTable(tables.Table):

    select = tables.CheckBoxColumn(accessor='pk')
    # select = MaterializeCssCheckboxColumn(accessor='pk')
    actions = tables.TemplateColumn(
        template_name='appprojeto1/buttons/actions.html',
        verbose_name='Ações',
        orderable=False,
        extra_context={
            'actions': {
                'edit': {
                    'text': 'Editar',
                    'icon': 'edit',
                    'route_url': 'AprovarCursosUpdateView',
                },
            }
        }
    )
    
    class Meta:
        model = Metas_efg

        fields = (
            'select',
            'diretoria',
            'escola',
            'tipo_curso',
            'curso',
            'turno',
            'modalidade',
            'vagas_totais',
            'carga_horaria',
            'situacao',
        )
        
        exclude = (
        )

        sequence = (
        )

        attrs = {
            "class": "table table-striped table-hover",
        }

        row_attrs = {"data-id": lambda record: record.pk}