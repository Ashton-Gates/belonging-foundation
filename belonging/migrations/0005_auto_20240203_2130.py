# Generated by Django 3.2.23 on 2024-02-04 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belonging', '0004_auto_20240203_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_internal_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('donor', 'Foundation Donor'), ('applicant', 'Scholarship Applicant'), ('recipient', 'Scholarship Recipient'), ('host', 'Auction Host'), ('bidder', 'Bidder'), ('owner', 'Local Shop Owner'), ('internal', 'Employee')], default='student', max_length=10),
        ),
    ]