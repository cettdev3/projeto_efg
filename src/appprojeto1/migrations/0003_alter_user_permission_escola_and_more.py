# Generated by Django 4.1.5 on 2023-01-24 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("appprojeto1", "0002_alter_cadastrar_curso_eixos"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_permission",
            name="escola",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="appprojeto1.metas_escolas",
            ),
        ),
        migrations.AlterField(
            model_name="user_permission",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="users_ids",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
