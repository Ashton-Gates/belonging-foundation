# Generated by Django 3.2.23 on 2024-02-12 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_otpmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='donoraccount',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
