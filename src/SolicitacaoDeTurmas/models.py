from multiselectfield import MultiSelectField
from django.db import models
from appprojeto1.models import Eixos, Cursos, Metas_escolas


class DefaultTable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SolicitacaoDeTurma(DefaultTable):
    TIPOS = (
        (0, "Capacitação"),
        (1, "Qualificação"),
        (2, "Técnico"),
        (3, "Superior"),
    )

    MODALIDADES = (
        ("PRESENCIAL", "Presencial"),
        ("ONLINE", "Online"),
        ("EAD", "EAD"),
    )

    TURNOS = (
        ("MATUTINO", "Matutino"),
        ("VESPERTINO", "Vespertino"),
        ("NOTURNO", "Noturno"),
    )

    TRIMESTRES = (
        ("PRIMEIRO", "Primeiro"),
        ("SEGUNDO", "Segundo"),
        ("TERCEIRO", "Terceiro"),
        ("QUARTO", "Quarto"),
    )

    SIM_NAO = (
        ("SIM", "Sim"),
        ("NAO", "Não"),
    )

    DIAS_SEMANA = (
        ("DOMINGO", "Domingo"),
        ("SEGUNDA", "Segunda"),
        ("TERCA", "Terça"),
        ("QUARTA", "Quarta"),
        ("QUINTA", "Quinta"),
        ("SEXTA", "Sexta"),
        ("SABADO", "Sábado"),
    )

    instace_id = models.CharField(
        max_length=40, null=True, blank=True, verbose_name="ID da instância de processo"
    )
    escola = models.ForeignKey(
        Metas_escolas,
        on_delete=models.DO_NOTHING,
        related_name="nome_escola",
        verbose_name="Nome da escola",
    )
    curso = models.ForeignKey(Cursos, on_delete=models.DO_NOTHING, verbose_name="Curso")
    eixo = models.ForeignKey(Eixos, on_delete=models.DO_NOTHING, verbose_name="Eixo")
    tipo = models.IntegerField(
        null=False, blank=False, choices=TIPOS, verbose_name="Tipo"
    )
    modalidade = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=MODALIDADES,
        verbose_name="Modalidade",
    )
    turno = models.CharField(
        max_length=255, null=False, blank=False, choices=TURNOS, verbose_name="Turno"
    )
    carga_horaria = models.IntegerField(
        null=False, blank=False, verbose_name="Carga horária"
    )
    vagas = models.IntegerField(null=False, blank=False, verbose_name="Vagas")
    fluxo_continuo = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=SIM_NAO,
        verbose_name="Fluxo contínuo",
    )
    previsao_inicio = models.DateField(
        max_length=255, null=False, blank=False, verbose_name="Previsão de início"
    )
    previsao_fim = models.DateField(
        max_length=255, null=False, blank=False, verbose_name="Previsão de fim"
    )
    dias_semana = MultiSelectField(
        max_length=255,
        null=False,
        blank=False,
        choices=DIAS_SEMANA,
        verbose_name="Dias da semana",
    )
    unidade_ensino = models.ForeignKey(
        Metas_escolas,
        on_delete=models.DO_NOTHING,
        related_name="unidade_ensino",
        verbose_name="Unidade de ensino",
    )

    def __str__(self) -> str:
        return super().__str__()

    class Meta:
        managed = True
        db_table = "solicitacaodeturma"
