# Generated by Django 3.2.23 on 2024-02-07 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belonging', '0013_auto_20240207_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarshipapplication',
            name='denial_feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendorapplication',
            name='denial_feedback',
            field=models.TextField(blank=True, null=True),
        ),
    ]
