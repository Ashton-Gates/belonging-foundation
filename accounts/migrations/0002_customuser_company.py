# Generated by Django 3.2.23 on 2024-02-29 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Company Name'),
        ),
    ]