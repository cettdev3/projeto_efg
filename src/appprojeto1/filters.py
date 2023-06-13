from django_filters import FilterSet, AllValuesFilter, ModelChoiceFilter, ChoiceFilter
from appprojeto1.models import Metas_efg, Metas_escolas, Cadastrar_curso
from DivisaoDeMetas.models import DivisaoDeMetasPorEscola
from appprojeto1.forms import DashboardAprovarCursosFilterModelForm
from django.db.models import Sum, Case, When, F


class AprovarCursosFilter(FilterSet):
    ano = AllValuesFilter()
    escola = ModelChoiceFilter(
        queryset=Metas_escolas.objects.filter(tipo__in=[0, 1]))
    curso = ModelChoiceFilter(queryset=Cadastrar_curso.objects.all())
    trimestre = AllValuesFilter()
    situacao = ChoiceFilter(
        choices=Metas_efg.situacao.field.choices[:-1])  # type: ignore

    class Meta:
        model = Metas_efg

        exclude = (
            'id',
            'num_edital',
        )


class DashboardAprovarCursosFilter(FilterSet):
    ano = AllValuesFilter()
    escola = ModelChoiceFilter(
        queryset=Metas_escolas.objects.filter(tipo__in=[0, 1]))
    curso = ModelChoiceFilter(
        queryset=Cadastrar_curso.objects.all().order_by('curso'))
    trimestre = AllValuesFilter()
    modalidade = AllValuesFilter()
    tipo_curso = AllValuesFilter()

    class Meta:
        model = Metas_efg

        form = DashboardAprovarCursosFilterModelForm

        exclude = (
            'id',
            'num_edital',
        )

    @property
    def vagas_totais_sum(self):

        vagas_totais_sum = self.qs.aggregate(
            Sum('vagas_totais'))['vagas_totais__sum']

        if vagas_totais_sum == None:
            vagas_totais_sum = 0

        return vagas_totais_sum

    @property
    def carga_horaria_total_sum(self):

        carga_horaria_total_sum = self.qs.aggregate(
            Sum('carga_horaria_total'))['carga_horaria_total__sum']

        if carga_horaria_total_sum == None:
            carga_horaria_total_sum = 0

        return carga_horaria_total_sum

    @property
    def recurso_planejado_sum(self):

        try:
            recurso_planejado_sum = round(self.qs.aggregate(
                carga_horaria_total__sum=Sum(
                    Case(
                        When(
                            modalidade_id=1,
                            then=F('carga_horaria_total') * 8.34
                        ),
                        default=F('carga_horaria_total') * 3.56
                    )
                )
            )['carga_horaria_total__sum'])
        except:
            recurso_planejado_sum = 0

        if recurso_planejado_sum == None:
            recurso_planejado_sum = 0

        return recurso_planejado_sum

    @property
    def saldo_de_horas_sum(self):
        saldo_de_horas_sum = DivisaoDeMetasPorEscola.objects.aggregate(
            carga_horaria__sum=Sum('carga_horaria')
        )['carga_horaria__sum']
        print(self.data)
        return 0
