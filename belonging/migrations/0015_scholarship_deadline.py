# Generated by Django 3.2.23 on 2024-02-07 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belonging', '0014_auto_20240207_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]