# Generated by Django 4.1.5 on 2023-04-10 19:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appprojeto1", "0011_alter_metas_efg_qualificacoes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="edital",
            name="pdf",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
