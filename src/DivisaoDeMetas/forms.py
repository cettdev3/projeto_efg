from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, Div
from crispy_forms.bootstrap import FormActions, StrictButton
from .models import DivisaoDeMetasPorEscola, Metas_escolas
from django import forms
from django.urls import reverse_lazy


class DivisaoDeMetasForm(forms.ModelForm):
    carga_horaria_total_atual = forms.IntegerField(
        widget=forms.HiddenInput(), required=False
    )

    def __init__(self, *args, **kwargs):
        super(DivisaoDeMetasForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Row(
                Column("escola", css_class="form-group col-md-6 mb-0"),
                Column("ano", css_class="form-group col-md-3 mb-0"),
                Column("semestre", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("tipo", css_class="form-group col-md-3 mb-0"),
                Column("modalidade", css_class="form-group col-md-3 mb-0"),
                Column("carga_horaria", css_class="form-group col-md-3 mb-0"),
                Column("carga_horaria_total", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            "carga_horaria_total_atual",
        )

        self.helper.layout.append(
            FormActions(
                Submit("save", "Salvar", css_class="btn-success"),
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-primary",
                    onclick="window.location.href = '{}';".format(
                        reverse_lazy("DivisaoDeMetasList")
                    ),
                ),
                css_class="d-flex justify-content-end",
            )
        )

        self.fields["escola"].queryset = Metas_escolas.objects.filter(tipo__in=[0, 1])

        self.fields["carga_horaria"].disabled = True

    class Meta:
        model = DivisaoDeMetasPorEscola

        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class DivisaoDeMetasFormDelete(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DivisaoDeMetasFormDelete, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Row(
                Column("escola", css_class="form-group col-md-6 mb-0"),
                Column("ano", css_class="form-group col-md-3 mb-0"),
                Column("semestre", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("tipo", css_class="form-group col-md-3 mb-0"),
                Column("modalidade", css_class="form-group col-md-3 mb-0"),
                Column("carga_horaria", css_class="form-group col-md-3 mb-0"),
                Column("carga_horaria_total", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
        )

        self.helper.layout.append(
            FormActions(
                Submit("submit", "Excluir", css_class="btn-danger"),
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-primary",
                    onclick="window.location.href = '{}';".format(
                        reverse_lazy("DivisaoDeMetasList")
                    ),
                ),
                css_class="d-flex justify-content-end",
            )
        )

        for field in self.fields:
            self.fields[field].disabled = True

    class Meta:
        model = DivisaoDeMetasPorEscola

        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class DivisaoDeMetasFilterFormHelper(FormHelper):
    form_method = "GET"  # type: ignore

    layout = Layout(
        Div(
            Div(
                Div("escola", css_class="flex-fill"),
                Div(
                    Div("ano", css_class="flex-fill"),
                    Div("semestre", css_class="flex-fill"),
                    Div("tipo", css_class="flex-fill"),
                    Div("modalidade", css_class="flex-fill"),
                    css_class="d-md-flex flex-fill gap-3",
                ),
                css_class="d-lg-flex flex-fill gap-3",
            ),
            Div(
                StrictButton(
                    '<i class="fas fa-search"></i>',
                    type="submit",
                    name="submit",
                    css_class="btn-outline-primary",
                ),
                StrictButton(
                    '<i class="fas fa-trash"></i>',
                    type="submit",
                    name="clean",
                    css_class="btn-outline-danger",
                ),
                css_class="d-flex flex-md-column-reverse mb-3 p-0 gap-1",
                # css_class='btn-group mb-3 p-0'
            ),
            css_class="form-row d-md-flex align-items-end overflow-auto gap-3",
        ),
    )
