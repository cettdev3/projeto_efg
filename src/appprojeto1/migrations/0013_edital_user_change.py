# Generated by Django 4.0.6 on 2023-04-12 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appprojeto1', '0012_alter_edital_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='edital',
            name='user_change',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
