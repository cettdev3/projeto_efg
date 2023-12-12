import django_tables2 as tables
from appprojeto1.models import Metas_efg


class AprovarCursosTable(tables.Table):
    id = tables.TemplateColumn(
        template_name="appprojeto1/input/input.html",
        verbose_name="",
        exclude_from_export=True,
    )

    checkbox = tables.CheckBoxColumn(
        accessor="pk",
        attrs={
            "th__input": {
                "onclick": "toggleAll(this)",
            },
            "td__input": {
                "onclick": "toggle(this)",
            },
        },
        orderable=False,
        exclude_from_export=True,
    )

    trimestre = tables.Column(visible=False)
    carga_horaria_total = tables.Column(visible=False)
    previsao_inicio = tables.DateColumn(visible=False)
    previsao_fim = tables.DateColumn(visible=False)
    previsao_abertura_edital = tables.DateColumn(visible=False)
    previsao_fechamento_edital = tables.DateColumn(visible=False)
    dias_semana = tables.Column(visible=False)

    actions = tables.TemplateColumn(
        template_name="appprojeto1/buttons/actions.html",
        verbose_name="Ações",
        orderable=False,
        extra_context={
            "actions": {
                "edit": {
                    "text": "Editar",
                    "icon": "edit",
                    "route_url": "AprovarCursosUpdateView",
                },
            }
        },
    )
    options = dict(Metas_efg.situacao.field.choices)  # type: ignore
    options.popitem()

    situacao = tables.TemplateColumn(
        template_name="appprojeto1/select/select.html",
        verbose_name="Situação",
        orderable=False,
        exclude_from_export=True,
        extra_context={
            "name": "situacao",
            "options": options,
        },
    )

    class Meta:
        model = Metas_efg

        fields = (
            "id",
            "checkbox",
            "diretoria",
            "escola",
            "tipo_curso",
            "curso",
            "turno",
            "modalidade",
            "trimestre",
            "vagas_totais",
            "carga_horaria",
            "carga_horaria_total",
            "previsao_inicio",
            "previsao_fim",
            "previsao_abertura_edital",
            "previsao_fechamento_edital",
            "dias_semana",
            "situacao",
        )

        exclude = ()

        sequence = ()

        attrs = {
            "class": "table table-striped table-hover prevent-select",
            "id": "table",
        }

        row_attrs = {
            "data-id": lambda record: record.pk,
        }
