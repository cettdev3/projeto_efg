import django_tables2 as tables
from django_tables2 import TemplateColumn
from DivisaoDeMetas.models import DivisaoDeMetasPorEscola


class DivisaoDeMetasTable(tables.Table):

    actions = TemplateColumn(
        template_name='DivisaoDeMetas/buttons/actions.html',
        verbose_name='Ações',
        orderable=False,
        extra_context={
            'actions': {
                'edit': { 
                    'text': 'Editar',
                    'icon': 'edit',
                    'route_url': 'DivisaoDeMetasUpdateView',
                },
                'delete': {
                    'text': 'Excluir',
                    'icon': 'trash',
                    'route_url': 'DivisaoDeMetasDeleteView',
                }
            }
        }
    )

    class Meta:
        model = DivisaoDeMetasPorEscola

        exclude = (
            'id',
            'created_at',
            'updated_at'
        )

        sequence = (
        )

        attrs = {
            "class": "table table-striped table-hover",
        }

        row_attrs = {"data-id": lambda record: record.pk}
