# Generated by Django 3.2.23 on 2024-02-29 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('donor', 'Foundation Donor'), ('applicant', 'Scholarship Applicant'), ('recipient', 'Scholarship Recipient'), ('host', 'Auction Host'), ('bidder', 'Bidder'), ('owner', 'Local Shop Owner'), ('internal', 'Employee'), ('vendor', 'Vendor'), ('sponsor', 'Sponsor'), ('distributor', 'Account Distributor'), ('venue', 'Venue'), ('other', 'Other')], default='other', max_length=30),
        ),
    ]
