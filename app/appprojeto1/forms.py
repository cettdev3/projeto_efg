from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django.forms.forms import Form
from django.forms import ModelForm
from crispy_forms.layout import Layout, Submit, Button
from crispy_forms.bootstrap import FormActions, StrictButton
from django.urls import reverse_lazy
from appprojeto1.models import Metas_efg, Metas_escolas, Eixos, Udepi_municipio, Cadastrar_curso
from appprojeto1.widgets import DatePickerInput


class AprovarCursosFilterFormHelper(FormHelper):

    form_method = 'GET'

    layout = Layout(
        Div(
            Div(
                Div('escola', css_class='flex-fill'),
                Div('curso', css_class='flex-fill'),
                css_class='d-lg-flex flex-fill gap-3'
            ),
            Div(
                Div('ano', css_class='flex-fill'),
                Div('trimestre', css_class='flex-fill'),
                Div('tipo_curso', css_class='flex-fill'),
                Div('modalidade', css_class='flex-fill'),
                Div('situacao', css_class='flex-fill'),
                css_class='d-md-flex flex-fill gap-3'
            ),
            Div(
                StrictButton('<i class="fas fa-search"></i>',
                             type='submit', name='submit', css_class='btn-outline-primary'),
                StrictButton('<i class="fas fa-trash"></i>',
                             type='submit', name='clean', css_class='btn-outline-danger'),
                css_class='d-flex flex-md-column-reverse mb-3 p-0 gap-1'
                # css_class='btn-group mb-3 p-0'
            ),
            css_class='form-row d-md-flex align-items-end overflow-auto gap-3'
        ),
    )


class AprovarCursosSubmitFormView(Form):
    def __init__(self, *args, **kwargs):
        super(AprovarCursosSubmitFormView, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(
            FormActions(
                StrictButton('<i class="fas fa-check"></i><spam> Aprovar</spam>',
                             type='submit', name='aprovar', value='3', css_class='btn-success'),
                StrictButton('<i class="fas fa-ban"></i><spam> Reprovar</spam>',
                             type='submit', name='aprovar', value='1', css_class='btn-danger'),
                StrictButton('<i class="far fa-hourglass"></i><spam> Em Análise</spam>',
                             type='submit', name='aprovar', value='2', css_class='btn-warning'),
                StrictButton('<i class="far fa-file"></i><spam> Gerar edital</spam>',
                             type='submit', name='edital', value='gerar', css_class='btn-primary'),
                css_class='d-flex justify-content-end gap-1'
            )
        )


class AprovarCursosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AprovarCursosForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div('diretoria', css_class='form-group flex-fill'),
                Div('escola', css_class='form-group flex-fill', 
                    onChange="populateDependentLists('{}')".format(
                                    reverse_lazy('ajax_load_municipios')
                            )),
                Div('udepi', css_class='form-group flex-fill'),
                css_class='form-row d-lg-flex flex-fill gap-3'
            ),
            Div(
                Div('tipo_curso', css_class='form-group flex-fill'),
                Div('modalidade', css_class='form-group flex-fill'),
                Div('turno', css_class='form-group flex-fill'),
                css_class='form-row d-lg-flex flex-fill gap-3'
            ),
            Div(
                Div('eixo', css_class='form-group flex-fill'),
                Div('curso', css_class='form-group flex-fill'),
                css_class='form-row d-lg-flex flex-fill gap-3'
            ),
            Div(
                Div('carga_horaria', css_class='form-group flex-fill'),
                Div('carga_horaria_total',
                    css_class='form-group flex-fill'),
                Div('vagas_turma', css_class='form-group flex-fill'),
                Div('vagas_totais', css_class='form-group flex-fill'),
                css_class='form-row d-lg-flex flex-fill gap-3'
            ),
            Div(
                Div('ano', css_class='form-group flex-fill'),
                Div('trimestre', css_class='form-group flex-fill'),
                Div('previsao_inicio', css_class='form-group flex-fill'),
                Div('previsao_fim', css_class='form-group flex-fill'),
                Div('dias_semana', css_class='form-group flex-fill'),
                # Div('previsao_abertura_edital',
                #     css_class='form-group flex-fill'),
                # Div('previsao_fechamento_edital',
                #     css_class='form-group flex-fill'),
                css_class='form-row d-lg-flex flex-fill gap-3'
            ),
        )

        self.helper.layout.append(
            FormActions(
                Submit(
                    'save', 'Salvar',
                    css_class='btn-success'
                ),
                Button(
                    'cancel', 'Cancelar',
                    css_class='btn-danger',
                    onclick="window.location.href = '{}';".format(
                        reverse_lazy('AprovarCursosView'))
                ),
                css_class='d-flex justify-content-end'
            )
        )

        self.fields['carga_horaria_total'].disabled = True

        self.fields['escola'].queryset = Metas_escolas.objects.filter(tipo=0)
        # self.fields['udepi'].queryset = Udepi_municipio.objects.none()
        # self.fields['eixo'].queryset = Eixos.objects.none()
        # self.fields['curso'].queryset = Cadastrar_curso.objects.none()

    class Meta:
        model = Metas_efg

        exclude = ('id', )
        
        labels = {
            'udepi': 'Cidade'
        }

        widgets = {
            'previsao_inicio': DatePickerInput(format=('%Y-%m-%d')),
            'previsao_fim': DatePickerInput(format=('%Y-%m-%d')),
            # 'previsao_abertura_edital': DatePickerInput(format=('%Y-%m-%d')),
            # 'previsao_fechamento_edital': DatePickerInput(format=('%Y-%m-%d')),
        }
        
    class Media:
        js = ('assets/js/populateDependentLists.js',)


class ReprovaCursosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReprovaCursosForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Div(
                Div('jus_reprovacao', css_class='form-group flex-fill'),
                css_class='form-row d-lg-flex flex-fill gap-3'
            ), 
        )
        self.helper.layout.append(
            FormActions(
                StrictButton('<i class="fas fa-ban"></i><spam> Reprovar</spam>',
                             type='submit', name='aprovar', value='1', css_class='btn-success'),
                StrictButton('<i class="fas fa-undo-alt"></i><spam> Cancelar</spam>',
                             type='button', name='cancel', value='cancel', css_class='btn-danger', 
                             onclick="window.location.href = '{}';".format(reverse_lazy('AprovarCursosView'))),
                css_class='d-flex justify-content-end gap-1'
            )
        )
        
        self.fields['jus_reprovacao'].required = True


    class Meta:
        model = Metas_efg
        
        fields = {
            'jus_reprovacao'
        }
        
        labels = {
            'jus_reprovacao': 'Justificativa para reprovação'
        }
