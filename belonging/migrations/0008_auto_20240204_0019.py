# Generated by Django 3.2.23 on 2024-02-04 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belonging', '0007_scholarshipapplication_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorapplication',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vendorapplication',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vendorapplication',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
    ]