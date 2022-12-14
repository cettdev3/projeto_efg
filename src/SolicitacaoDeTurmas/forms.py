from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from crispy_forms.bootstrap import FormActions, InlineCheckboxes, InlineRadios
from django import forms
from .widgets import DatePickerInput
from .models import Curso, Escola, SolicitacaoDeTurma, Eixo


class SolicitacaoDeTurmas(forms.ModelForm):
    
    udepi = forms.ChoiceField(
        choices=(('SIM','Sim'),('NAO','Não')),
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super(SolicitacaoDeTurmas, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        
        self.helper.layout = Layout(
            Row(
                Column('escola', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('tipo', css_class='form-group col-md-4 mb-0'),
                Column('modalidade', css_class='form-group col-md-4 mb-0'),
                Column('turno', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('eixo', css_class='form-group col-md-4 mb-0'),
                Column('curso', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('carga_horaria', css_class='form-group col-md-4 mb-0'),
                Column('vagas', css_class='form-group col-md-4 mb-0'),
                Column('fluxo_continuo',
                       css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('previsao_inicio',
                       css_class='form-group col-md-3 mb-0'),
                Column('previsao_fim', css_class='form-group col-md-3 mb-0'),
                Column(InlineCheckboxes('dias_semana'), css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(InlineRadios('udepi'), css_class='form-group col-md-2 mb-0'),
                Column('unidade_ensino', css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            )
        )
        
        self.helper.layout.append(
            FormActions(
                    Submit('save', 'Salvar', css_class='btn-primary'),
                    Button('cancel', 'Cancelar', css_class='btn-danger'),
                    css_class='d-flex justify-content-end'
            )
        )
        
        self.fields['escola'].queryset = Escola.objects.filter(tipo=0)
        
        self.fields['unidade_ensino'].queryset = Escola.objects.filter(tipo=2)
        
        self.fields['curso'].queryset = Curso.objects.none()
            
    class Meta:
        model = SolicitacaoDeTurma

        fields = (
            'escola',
            'curso',
            'eixo',
            'tipo',
            'modalidade',
            'turno',
            'carga_horaria',
            'vagas',
            'fluxo_continuo',
            'previsao_inicio',
            'previsao_fim',
            'dias_semana',
            'unidade_ensino',
        )

        labels = {
            'unidade_ensino': 'Nome da UDEPI',
        }

        widgets = {
            'previsao_inicio': DatePickerInput(),
            'previsao_fim': DatePickerInput(),
        }