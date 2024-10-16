from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Button, Field
from django.forms.forms import Form
from django.forms import ModelForm
from crispy_forms.bootstrap import FormActions, StrictButton
from django.urls import reverse_lazy
from appprojeto1.models import Metas_efg, Metas_escolas, Cadastrar_curso
from appprojeto1.widgets import DatePickerInput


class AprovarCursosFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AprovarCursosFilterFormHelper, self).__init__(*args, **kwargs)

        self.form_method = "GET"

        self.layout = Layout(
            Div(
                Div(
                    Div(
                        Div(
                            Field("escola", onChange="populateDependentLists(this)"),
                            css_class="flex-fill",
                        ),
                        Div(
                            Field(
                                "tipo_curso", onChange="populateDependentLists(this)"
                            ),
                            css_class="flex-fill",
                        ),
                        Div(
                            Field(
                                "modalidade", onChange="populateDependentLists(this)"
                            ),
                            css_class="flex-fill",
                        ),
                        css_class="d-md-flex flex-fill gap-3",
                    ),
                    Div(
                        Div(Field("curso"), css_class="flex-fill"),
                        Div(Field("ano"), css_class="flex-fill"),
                        Div(Field("trimestre"), css_class="flex-fill"),
                        Div(Field("situacao"), css_class="flex-fill"),
                        css_class="d-md-flex flex-fill gap-3",
                    ),
                    css_class="flex-fill gap-3",
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
                    # css_class='btn-group mb-3 p-0',
                ),
                css_class="form-row d-md-flex align-items-end " "flex-fill gap-3",
            ),
        )

    class Media:
        js = ("assets/js/populateDependentLists.js",)


class AprovarCursosSubmitFormView(Form):
    def __init__(self, *args, **kwargs):
        super(AprovarCursosSubmitFormView, self).__init__(*args, **kwargs)

        ApprovalList = set(
            Metas_efg.objects.filter(situacao__in=[0, 1, 2, 3]).values_list(
                "situacao", flat=True
            )
        )

        ApprovalLen = len(ApprovalList)

        if len(ApprovalList) > 0:
            ApprovalType = list(ApprovalList)[0]
        else:
            ApprovalType = list()

        disable_edital = True

        if ApprovalLen == 1 and ApprovalType == 3:
            disable_edital = False

        self.helper = FormHelper(self)

        self.helper.layout.append(  # type: ignore
            FormActions(
                StrictButton(
                    '<i class="fas fa-check-square"></i><spam> Aprovar</spam>',
                    id="aprovar_selecionados",
                    type="submit",
                    name="aprovar_selecionados",
                    value="3",
                    css_class="btn-success",
                    disabled=True,
                ),
                StrictButton(
                    '<i class="fas fa-save"></i><spam> Salvar</spam>',
                    type="submit",
                    name="aprovar",
                    value="3",
                    css_class="btn-success",
                ),
                StrictButton(
                    '<i class="far fa-file"></i><spam> Gerar edital</spam>',
                    type="submit",
                    name="edital",
                    value="gerar",
                    css_class="btn-primary",
                    disabled=disable_edital,
                ),
                css_class="d-flex justify-content-end gap-1",
            )
        )


class AprovarCursosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AprovarCursosForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div(Field("diretoria"), css_class="form-group flex-fill"),
                Div(
                    Field("escola", onChange="populateDependentLists(this)"),
                    css_class="form-group flex-fill",
                ),
                Div(Field("udepi"), css_class="form-group flex-fill"),
                css_class="form-row d-lg-flex flex-fill gap-3",
            ),
            Div(
                Div(
                    Field("tipo_curso", onChange="populateDependentLists(this)"),
                    css_class="form-group flex-fill",
                ),
                Div(
                    Field("modalidade", onChange="populateDependentLists(this)"),
                    css_class="form-group flex-fill",
                ),
                Div(Field("turno"), css_class="form-group flex-fill"),
                css_class="form-row d-lg-flex flex-fill gap-3",
            ),
            Div(
                Div(
                    Field("eixo", onchange="populateDependentLists(this)"),
                    css_class="form-group flex-fill",
                ),
                Div(Field("curso"), css_class="form-group flex-fill"),
                css_class="form-row d-lg-flex flex-fill gap-3",
            ),
            Div(
                Div(Field("carga_horaria"), css_class="form-group flex-fill"),
                Div(Field("carga_horaria_total"), css_class="form-group flex-fill"),
                # Div(Field('vagas_turma', css_class='form-group flex-fill'),
                Div(Field("vagas_totais"), css_class="form-group flex-fill"),
                css_class="form-row d-lg-flex flex-fill gap-3",
            ),
            Div(
                Div(Field("ano"), css_class="form-group flex-fill"),
                Div(Field("trimestre"), css_class="form-group flex-fill"),
                Div(Field("previsao_inicio"), css_class="form-group flex-fill"),
                Div(Field("previsao_fim"), css_class="form-group flex-fill"),
                Div(Field("dias_semana"), css_class="form-group flex-fill"),
                # Div('previsao_abertura_edital',
                #     css_class='form-group flex-fill'),
                # Div('previsao_fechamento_edital',
                #     css_class='form-group flex-fill'),
                css_class="form-row d-lg-flex flex-fill gap-3",
            ),
        )

        self.helper.layout.append(
            FormActions(
                Submit("save", "Salvar", css_class="btn-success"),
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-danger",
                    onclick="window.location.href = '{}';".format(
                        reverse_lazy("AprovarCursosView")
                    ),
                ),
                css_class="d-flex justify-content-end",
            )
        )

        self.fields["carga_horaria_total"].disabled = True

        self.fields["escola"].queryset = Metas_escolas.objects.filter(tipo__in=[0, 1])
        # self.fields['udepi'].queryset = Udepi_municipio.objects.none()
        # self.fields['eixo'].queryset = Eixos.objects.none()
        # self.fields['curso'].queryset = Cadastrar_curso.objects.none()

    class Meta:
        model = Metas_efg

        exclude = ("id",)

        labels = {"udepi": "Cidade"}

        widgets = {
            "previsao_inicio": DatePickerInput(format=("%Y-%m-%d")),
            "previsao_fim": DatePickerInput(format=("%Y-%m-%d")),
            # 'previsao_abertura_edital': DatePickerInput(
            #     format=('%Y-%m-%d')),
            # 'previsao_fechamento_edital': DatePickerInput(
            #     format=('%Y-%m-%d')),
        }

    class Media:
        js = ("assets/js/populateDependentLists.js",)


class ReprovaCursosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReprovaCursosForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div("jus_reprovacao", css_class="form-group flex-fill"),
                css_class="form-row d-lg-flex flex-fill gap-3",
            ),
        )
        self.helper.layout.append(
            FormActions(
                StrictButton(
                    '<i class="fas fa-ban"></i><spam> Reprovar</spam>',
                    type="submit",
                    name="aprovar",
                    value="1",
                    css_class="btn-success",
                ),
                StrictButton(
                    '<i class="fas fa-undo-alt"></i><spam> Cancelar</spam>',
                    type="button",
                    name="cancel",
                    value="cancel",
                    css_class="btn-danger",
                    onclick="window.location.href = '{}';".format(
                        reverse_lazy("AprovarCursosView")
                    ),
                ),
                css_class="d-flex justify-content-end gap-1",
            )
        )

        self.fields["jus_reprovacao"].required = True

    class Meta:
        model = Metas_efg

        fields = {"jus_reprovacao"}

        labels = {"jus_reprovacao": "Justificativa para reprovação"}


class DashboardAprovarCursosFilterModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DashboardAprovarCursosFilterModelForm, self).__init__(*args, **kwargs)

        if (
            (self.data.get("escola"))
            and (self.data.get("modalidade"))
            and (self.data.get("tipo_curso"))
        ):
            try:
                escola_id = int(self.data.get("escola"))  # type: ignore
                modalidade_id = int(self.data.get("modalidade"))  # type: ignore
                tipo_id = int(self.data.get("tipo_curso"))  # type: ignore
                self.fields["curso"].queryset = Cadastrar_curso.objects.filter(
                    escola_id=escola_id,
                    modalidade_id=modalidade_id,
                    tipo_id=tipo_id,
                ).order_by("curso")
                self.fields["curso"].disabled = False

            except (ValueError, TypeError):
                self.fields["curso"].queryset = Cadastrar_curso.objects.none()
                self.fields["curso"].disabled = True
        else:
            self.fields["curso"].queryset = Cadastrar_curso.objects.none()
            self.fields["curso"].disabled = True

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        Div("ano", css_class=""),
                        Div("trimestre", css_class=""),
                        Div("escola", css_class=""),
                        css_class="col gap-3",
                    ),
                    Div(
                        Div("modalidade", css_class=""),
                        Div("tipo_curso", css_class=""),
                        Div("curso", css_class=""),
                        css_class="col gap-3",
                    ),
                    css_class="d-md-flex gap-3",
                ),
                Div(
                    StrictButton(
                        "Filtrar", type="submit", name="submit", css_class="btn-primary"
                    ),
                    StrictButton(
                        "Redefinir filtro",
                        type="submit",
                        name="clean",
                        css_class="btn-danger",
                    ),
                    # css_class='d-flex flex-md-column-reverse mb-3 p-0 gap-1'
                    css_class="d-flex justify-content-end gap-2",
                ),
                css_class="form-row align-items-end overflow-auto gap-3",
            ),
        )

    class Meta:
        model = Metas_efg

        fields = {"ano", "trimestre", "escola", "modalidade", "curso", "tipo_curso"}
