import django_tables2 as tables
from appprojeto1.models import Metas_efg
from django.db.models import Q

class AprovarCursosTable(tables.Table):

    id = tables.TemplateColumn(
        template_name='appprojeto1/input/input.html',
        verbose_name='',
    )    
    
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
    options = dict(Metas_efg.situacao.field.choices)  # type: ignore
    options.popitem()
    
    situacao = tables.TemplateColumn(
        template_name='appprojeto1/select/select.html',
        verbose_name='Situação',
        orderable=False,
        extra_context={
            'name': 'situacao',
            'options':
                options,
        }
    )
    
    class Meta:
        model = Metas_efg
        
        fields = (
            'id',
            # 'select',
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

        row_attrs = {
            "data-id": lambda record: record.pk,
        }