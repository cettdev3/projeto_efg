# Generated by Django 4.0.6 on 2023-08-10 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appprojeto1', '0020_saldo_replanejamento_ano_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saldo_replanejamento',
            name='ano',
        ),
        migrations.RemoveField(
            model_name='saldo_replanejamento',
            name='semestre',
        ),
    ]
