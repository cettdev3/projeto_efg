from multiselectfield import MultiSelectField
from django.db import models


class DefaultTable(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Eixo(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=60, null=False, blank=False)

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = 'eixos'


class Curso(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo_id = models.IntegerField(null=False, blank=False)
    eixos = models.ForeignKey(Eixo, on_delete=models.DO_NOTHING)
    curso = models.CharField(max_length=100, null=False, blank=False)
    status = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.curso

    class Meta:
        managed = False
        db_table = 'cursos'


class Escola(models.Model):

    TIPO = (
        (0, 'EFG'),
        (1, 'COTEC'),
        (2, 'UDEPI'),
        (3, 'CVT'),
        (4, 'Salas de Extensão'),
    )

    id = models.IntegerField(primary_key=True)
    escola = models.CharField(max_length=255, null=False, blank=False)
    tipo = models.IntegerField(null=False, blank=False, choices=TIPO)

    def __str__(self):
        return self.escola

    class Meta:
        managed = False
        db_table = 'escolas'


class SolicitacaoDeTurma(DefaultTable):

    TIPOS = (
        (0, 'Capacitação'),
        (1, 'Qualificação'),
        (2, 'Técnico'),
        (3, 'Superior'),
    )

    MODALIDADES = (
        ('PRESENCIAL', 'Presencial'),
        ('ONLINE', 'Online'),
        ('EAD', 'EAD'),
    )

    TURNOS = (
        ('MATUTINO', 'Matutino'),
        ('VESPERTINO', 'Vespertino'),
        ('NOTURNO', 'Noturno'),
    )

    TRIMESTRES = (
        ('PRIMEIRO', 'Primeiro'),
        ('SEGUNDO', 'Segundo'),
        ('TERCEIRO', 'Terceiro'),
        ('QUARTO', 'Quarto'),
    )

    SIM_NAO = (
        ('SIM', 'Sim'),
        ('NAO', 'Não'),
    )

    DIAS_SEMANA = (
        ('DOMINGO', 'Domingo'),
        ('SEGUNDA', 'Segunda'),
        ('TERCA', 'Terça'),
        ('QUARTA', 'Quarta'),
        ('QUINTA', 'Quinta'),
        ('SEXTA', 'Sexta'),
        ('SABADO', 'Sábado'),
    )

    instace_id = models.CharField(
        max_length=40, null=True, blank=True, verbose_name='ID da instância de processo')
    escola = models.ForeignKey(
        Escola, on_delete=models.DO_NOTHING, related_name='escolas', verbose_name='Nome da escola')
    curso = models.ForeignKey(
        Curso, on_delete=models.DO_NOTHING, verbose_name='Curso')
    eixo = models.ForeignKey(
        Eixo, on_delete=models.DO_NOTHING, verbose_name='Eixo')
    tipo = models.IntegerField(null=False, blank=False,
                            choices=TIPOS, verbose_name='Tipo')
    modalidade = models.CharField(max_length=255, null=False, blank=False,
                                  choices=MODALIDADES, verbose_name='Modalidade')
    turno = models.CharField(max_length=255, null=False, blank=False,
                             choices=TURNOS, verbose_name='Turno')
    carga_horaria = models.IntegerField(
        null=False, blank=False, verbose_name='Carga horária')
    vagas = models.IntegerField(null=False, blank=False, verbose_name='Vagas')
    fluxo_continuo = models.CharField(
        max_length=255, null=False, blank=False, choices=SIM_NAO, verbose_name='Fluxo contínuo')
    previsao_inicio = models.DateField(
        max_length=255, null=False, blank=False, verbose_name='Previsão de início')
    previsao_fim = models.DateField(
        max_length=255, null=False, blank=False, verbose_name='Previsão de fim')
    dias_semana = MultiSelectField(max_length=255, null=False, blank=False,
                                   choices=DIAS_SEMANA, verbose_name='Dias da semana')
    unidade_ensino = models.ForeignKey(
        Escola, on_delete=models.DO_NOTHING, related_name='unidade_ensino', verbose_name='Unidade de ensino')

    def __str__(self) -> str:
        return super().__str__()

    class Meta:
        managed = True
        db_table = 'solicitacaodeturma'
