from email.policy import default
from random import choices
from django.db import models
from django.urls import reverse_lazy


class DefaultTable(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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


class TipoCurso(models.Model):

    TIPOS = (
        (0, 'Capacitação'),
        (1, 'Qualificação'),
        (2, 'Técnico'),
        (3, 'Superior'),
    )

    id = models.IntegerField(primary_key=True)
    tipo = models.IntegerField(null=False, blank=False, choices=TIPOS)

    def __str__(self):
        return self.tipo

    class Meta:
        managed = False
        db_table = 'tipo_curso'


class Modalidade(models.Model):

    MODALIDADES = (
        (1, 'Presencial'),
        (2, 'Online'),
        (3, 'EAD'),
    )

    id = models.IntegerField(primary_key=True)
    modalidade = models.IntegerField(
        null=False, blank=False, choices=MODALIDADES)

    def __str__(self):
        return self.modalidade

    class Meta:
        managed = False
        db_table = 'modalidade'


class DivisaoDeMetasPorEscola(DefaultTable):
    SEMESTRE = (
        (1, '1º Semestre'),
        (2, '2º Semestre'),
    )

    escola = models.ForeignKey(
        Escola, on_delete=models.DO_NOTHING, related_name='escolas', verbose_name='Nome da escola', help_text='Escola para execução da meta')
    ano = models.IntegerField(
        null=False, blank=False, verbose_name='Ano', help_text='Ano de execução da meta')
    semestre = models.IntegerField(
        null=False, blank=False, choices=SEMESTRE, verbose_name='Semestre', help_text='Semestre de execução da meta')
    tipo = models.ForeignKey(
        TipoCurso, on_delete=models.DO_NOTHING, verbose_name='Tipo', help_text='Tipo do curso')
    modalidade = models.ForeignKey(
        Modalidade, on_delete=models.DO_NOTHING, verbose_name='Modalidade', help_text='Modalidade de execução do curso')
    carga_horaria = models.PositiveIntegerField(
        null=False, blank=False, verbose_name='Ch. disp.', default=0, help_text='Carga horária disponível')
    carga_horaria_total = models.PositiveIntegerField(
        null=False, blank=False, verbose_name='Ch. total', default=0, help_text='Carga horária total')

    def get_absolute_url(self):
        return reverse_lazy('DivisaoDeMetasList')

    class Meta:
        managed = True
        db_table = 'divisaodemetasporescola'
        ordering = ['-id']
