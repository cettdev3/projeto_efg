# Generated by Django 4.0.6 on 2023-08-10 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appprojeto1', '0021_remove_saldo_replanejamento_ano_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='saldo_replanejamento',
            name='ano',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='saldo_replanejamento',
            name='semestre',
            field=models.IntegerField(default=None),
        ),
    ]
