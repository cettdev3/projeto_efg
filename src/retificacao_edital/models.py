from django.db import models
from appprojeto1.models import (
    Metas_escolas,
    Metas_tipo,
    Cadastrar_curso,
    Metas_modalidade,
    Eixos,
    Udepi_municipio,
    Edital,
    Metas_efg,
)
from django.contrib.auth.models import User



# Create your models here.
class Editais_Retificados(models.Model):
    id = models.AutoField(primary_key=True)
    num_edital = models.IntegerField()
    ano = models.IntegerField()
    dt_ini_edit = models.DateField(null=True, blank=True)
    dt_fim_edit = models.DateField(null=True, blank=True)
    dt_ini_insc = models.DateField(null=True, blank=True)
    dt_fim_insc = models.DateField(null=True, blank=True)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    pdf = models.CharField(max_length=255, null=True, blank=True)
    motivo = models.CharField(max_length=255, blank=False, null=True)
    user_change = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    edital_origem = models.ForeignKey(Edital, on_delete=models.DO_NOTHING, null=True)
    saldo_disponivel = models.IntegerField(default=0)

    def __str__(self):
        return self.num_edital

    class Meta:
        managed = True
        db_table = "editais_retificados"


class Turmas_Retificadas(models.Model):
    SITUACAO = (
        (0, "Aguardando Análise"),
        (1, "Reprovado"),
        (2, "Em Análise"),
        (3, "Aprovado"),
        (4, "Edital gerado"),
        (5, "Replanejado"),
    )

    DIRETORIAS = (
        ("DAC", "DAC"),
        ("DDA", "DDA"),
        ("DE", "DE"),
    )

    SEMESTRES = (
        (1, "1º SEMESTRE"),
        (2, "2º SEMESTRE"),
    )

    TURNOS = (
        ("MATUTINO", "MATUTINO"),
        ("VESPERTINO", "VESPERTINO"),
        ("NOTURNO", "NOTURNO"),
        ("INTEGRAL", "INTEGRAL"),
    )

    id = models.AutoField(primary_key=True)
    diretoria = models.CharField(max_length=255, choices=DIRETORIAS, null=True)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE, null=True)
    tipo_curso = models.ForeignKey(Metas_tipo, on_delete=models.CASCADE, null=True)
    curso = models.ForeignKey(Cadastrar_curso, on_delete=models.CASCADE, null=True)
    turno = models.CharField(max_length=255, choices=TURNOS, null=True)
    ano = models.IntegerField()
    modalidade = models.ForeignKey(Metas_modalidade, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=SEMESTRES, null=True)
    vagas_totais = models.IntegerField(null=True)
    carga_horaria = models.IntegerField(null=True)
    carga_horaria_total = models.IntegerField(null=True)
    previsao_inicio = models.DateField(null=True)
    previsao_fim = models.DateField(null=True)
    dias_semana = models.CharField(max_length=255)
    previsao_abertura_edital = models.DateField(null=True, blank=True)
    previsao_fechamento_edital = models.DateField(null=True, blank=True)
    data_registro = models.DateField(null=True, blank=True)
    eixo = models.ForeignKey(Eixos, on_delete=models.CASCADE, null=True)
    udepi = models.ForeignKey(Udepi_municipio, on_delete=models.CASCADE, null=True)
    situacao = models.IntegerField(default=0, choices=SITUACAO, null=True, blank=True)
    jus_reprovacao = models.TextField(default=None, null=True, blank=True)
    num_edital = models.ForeignKey(
        Editais_Retificados,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    curso_tecnico = models.CharField(
        default=None, null=True, blank=True, max_length=255
    )
    qualificacoes = models.CharField(default="", null=True, blank=True, max_length=255)
    origem_replan = models.ForeignKey(
        Metas_efg, on_delete=models.CASCADE, default=None, null=True, blank=True
    )

    class Meta:
        managed = True
        db_table = "turmas_retificadas"
