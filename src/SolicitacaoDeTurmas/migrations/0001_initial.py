# Generated by Django 4.1.4 on 2023-01-17 18:01

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("appprojeto1", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SolicitacaoDeTurma",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "instace_id",
                    models.CharField(
                        blank=True,
                        max_length=40,
                        null=True,
                        verbose_name="ID da instância de processo",
                    ),
                ),
                (
                    "tipo",
                    models.IntegerField(
                        choices=[
                            (0, "Capacitação"),
                            (1, "Qualificação"),
                            (2, "Técnico"),
                            (3, "Superior"),
                        ],
                        verbose_name="Tipo",
                    ),
                ),
                (
                    "modalidade",
                    models.CharField(
                        choices=[
                            ("PRESENCIAL", "Presencial"),
                            ("ONLINE", "Online"),
                            ("EAD", "EAD"),
                        ],
                        max_length=255,
                        verbose_name="Modalidade",
                    ),
                ),
                (
                    "turno",
                    models.CharField(
                        choices=[
                            ("MATUTINO", "Matutino"),
                            ("VESPERTINO", "Vespertino"),
                            ("NOTURNO", "Noturno"),
                        ],
                        max_length=255,
                        verbose_name="Turno",
                    ),
                ),
                ("carga_horaria", models.IntegerField(verbose_name="Carga horária")),
                ("vagas", models.IntegerField(verbose_name="Vagas")),
                (
                    "fluxo_continuo",
                    models.CharField(
                        choices=[("SIM", "Sim"), ("NAO", "Não")],
                        max_length=255,
                        verbose_name="Fluxo contínuo",
                    ),
                ),
                (
                    "previsao_inicio",
                    models.DateField(max_length=255, verbose_name="Previsão de início"),
                ),
                (
                    "previsao_fim",
                    models.DateField(max_length=255, verbose_name="Previsão de fim"),
                ),
                (
                    "dias_semana",
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[
                            ("DOMINGO", "Domingo"),
                            ("SEGUNDA", "Segunda"),
                            ("TERCA", "Terça"),
                            ("QUARTA", "Quarta"),
                            ("QUINTA", "Quinta"),
                            ("SEXTA", "Sexta"),
                            ("SABADO", "Sábado"),
                        ],
                        max_length=255,
                        verbose_name="Dias da semana",
                    ),
                ),
                (
                    "curso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="appprojeto1.cursos",
                        verbose_name="Curso",
                    ),
                ),
                (
                    "eixo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="appprojeto1.eixos",
                        verbose_name="Eixo",
                    ),
                ),
                (
                    "escola",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="nome_escola",
                        to="appprojeto1.metas_escolas",
                        verbose_name="Nome da escola",
                    ),
                ),
                (
                    "unidade_ensino",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="unidade_ensino",
                        to="appprojeto1.metas_escolas",
                        verbose_name="Unidade de ensino",
                    ),
                ),
            ],
            options={
                "db_table": "solicitacaodeturma",
                "managed": True,
            },
        ),
    ]
