from django.db import models
from django.urls import reverse_lazy
from appprojeto1.models import Metas_escolas, Metas_tipo, Metas_modalidade


class DefaultTable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DivisaoDeMetasPorEscola(DefaultTable):
    SEMESTRE = (
        (1, "1º Semestre"),
        (2, "2º Semestre"),
    )

    escola = models.ForeignKey(
        Metas_escolas,
        on_delete=models.DO_NOTHING,
        related_name="escolas",
        verbose_name="Nome da escola",
        help_text="Escola para execução da meta",
    )
    ano = models.IntegerField(
        null=False, blank=False, verbose_name="Ano", help_text="Ano de execução da meta"
    )
    semestre = models.IntegerField(
        null=False,
        blank=False,
        choices=SEMESTRE,
        verbose_name="Semestre",
        help_text="Semestre de execução da meta",
    )
    tipo = models.ForeignKey(
        Metas_tipo,
        on_delete=models.DO_NOTHING,
        verbose_name="Tipo",
        help_text="Tipo do curso",
    )
    modalidade = models.ForeignKey(
        Metas_modalidade,
        on_delete=models.DO_NOTHING,
        verbose_name="Modalidade",
        help_text="Modalidade de execução do curso",
    )
    carga_horaria = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Ch. disp.",
        default=0,
        help_text="Carga horária disponível",
    )
    carga_horaria_total = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Ch. total",
        default=0,
        help_text="Carga horária total",
    )

    def get_absolute_url(self):
        return reverse_lazy("DivisaoDeMetasList")

    class Meta:
        managed = True
        db_table = "divisaodemetasporescola"
        ordering = ["-id"]
