# Generated by Django 4.0.6 on 2023-10-04 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appprojeto1', '0023_metas_efg_origem_replan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editais_Retificados',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num_edital', models.IntegerField()),
                ('ano', models.IntegerField()),
                ('dt_ini_edit', models.DateField(blank=True, null=True)),
                ('dt_fim_edit', models.DateField(blank=True, null=True)),
                ('dt_ini_insc', models.DateField(blank=True, null=True)),
                ('dt_fim_insc', models.DateField(blank=True, null=True)),
                ('status', models.CharField(max_length=255)),
                ('pdf', models.CharField(blank=True, max_length=255, null=True)),
                ('motivo', models.CharField(max_length=255, null=True)),
                ('edital_origem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='appprojeto1.edital')),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appprojeto1.metas_escolas')),
                ('user_change', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'editais_retificados',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Turmas_Retificadas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('diretoria', models.CharField(choices=[('DAC', 'DAC'), ('DDA', 'DDA'), ('DE', 'DE')], max_length=255, null=True)),
                ('turno', models.CharField(choices=[('MATUTINO', 'MATUTINO'), ('VESPERTINO', 'VESPERTINO'), ('NOTURNO', 'NOTURNO'), ('INTEGRAL', 'INTEGRAL')], max_length=255, null=True)),
                ('ano', models.IntegerField()),
                ('trimestre', models.IntegerField(choices=[(1, '1º SEMESTRE'), (2, '2º SEMESTRE')], null=True)),
                ('vagas_totais', models.IntegerField(null=True)),
                ('carga_horaria', models.IntegerField(null=True)),
                ('carga_horaria_total', models.IntegerField(null=True)),
                ('previsao_inicio', models.DateField(null=True)),
                ('previsao_fim', models.DateField(null=True)),
                ('dias_semana', models.CharField(max_length=255)),
                ('previsao_abertura_edital', models.DateField(blank=True, null=True)),
                ('previsao_fechamento_edital', models.DateField(blank=True, null=True)),
                ('data_registro', models.DateField(blank=True, null=True)),
                ('situacao', models.IntegerField(blank=True, choices=[(0, 'Aguardando Análise'), (1, 'Reprovado'), (2, 'Em Análise'), (3, 'Aprovado'), (4, 'Edital gerado'), (5, 'Replanejado')], default=0, null=True)),
                ('jus_reprovacao', models.TextField(blank=True, default=None, null=True)),
                ('curso_tecnico', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('qualificacoes', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('origem_replan', models.IntegerField(null=True)),
                ('curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appprojeto1.cadastrar_curso')),
                ('eixo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appprojeto1.eixos')),
                ('escola', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appprojeto1.metas_escolas')),
                ('modalidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appprojeto1.metas_modalidade')),
                ('num_edital', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='retificacao_edital.editais_retificados')),
                ('tipo_curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appprojeto1.metas_tipo')),
                ('udepi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appprojeto1.udepi_municipio')),
            ],
            options={
                'db_table': 'turmas_retificadas',
                'managed': True,
            },
        ),
    ]
