# Generated by Django 4.1.4 on 2023-01-10 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("appprojeto1", "0006_alter_cursos_table_alter_solicitacao_table"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="metas_efg",
            options={"managed": True},
        ),
        migrations.RemoveField(
            model_name="metas_efg",
            name="descricao",
        ),
        migrations.RemoveField(
            model_name="metas_efg",
            name="repasse",
        ),
        migrations.RemoveField(
            model_name="metas_efg",
            name="valor_unitario",
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="curso",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="appprojeto1.cadastrar_curso",
            ),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="data_registro",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="eixo",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="appprojeto1.eixos",
            ),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="jus_reprovacao",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="num_edital",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="appprojeto1.edital",
            ),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="previsao_abertura_edital",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="previsao_fechamento_edital",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="previsao_fim",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="previsao_inicio",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="situacao",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Aguardando Análise"),
                    (1, "Reprovado"),
                    (2, "Em Análise"),
                    (3, "Aprovado"),
                    (4, "Edital gerado"),
                ],
                default=0,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="tipo_curso",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="appprojeto1.metas_tipo",
            ),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="trimestre",
            field=models.IntegerField(
                choices=[(1, "1º SEMESTRE"), (2, "2º SEMESTRE")], null=True
            ),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="turno",
            field=models.CharField(
                choices=[
                    ("MATUTINO", "MATUTINO"),
                    ("VESPERTINO", "VESPERTINO"),
                    ("NOTURNO", "NOTURNO"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="udepi",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="appprojeto1.udepi_municipio",
            ),
        ),
        migrations.AddField(
            model_name="metas_efg",
            name="vagas_totais",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="metas_efg",
            name="carga_horaria",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="metas_efg",
            name="carga_horaria_total",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="metas_efg",
            name="diretoria",
            field=models.CharField(
                choices=[("DAC", "DAC"), ("DDA", "DDA"), ("DE", "DE")],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="metas_efg",
            name="escola",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="appprojeto1.metas_escolas",
            ),
        ),
        migrations.AlterField(
            model_name="metas_efg",
            name="modalidade",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="appprojeto1.metas_modalidade",
            ),
        ),
        migrations.AlterModelTable(
            name="metas_efg",
            table="Turmas_planejado_orcado",
        ),
    ]
