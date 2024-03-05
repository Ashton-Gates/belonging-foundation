# Generated by Django 3.2.23 on 2024-03-05 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0004_rename_scholarship_scholarship_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='grand_prize',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='second_prize',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='third_place',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
