# Generated by Django 3.2.23 on 2024-02-07 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belonging', '0010_auto_20240206_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarshipapplication',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]