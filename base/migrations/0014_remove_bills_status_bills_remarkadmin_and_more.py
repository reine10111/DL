# Generated by Django 4.2.7 on 2023-11-26 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_remove_submission_remarks_bills_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bills',
            name='status',
        ),
        migrations.AddField(
            model_name='bills',
            name='remarkAdmin',
            field=models.CharField(choices=[('Pending', 'Pending'), ('NotPaid', 'Not Paid'), ('Paid', 'Paid')], default='Pending', max_length=10),
        ),
        migrations.AddField(
            model_name='bills',
            name='remarkMember',
            field=models.CharField(choices=[('Pending', 'Pending'), ('NotPaid', 'Not Paid'), ('Paid', 'Paid')], default='NotPaid', max_length=10),
        ),
    ]
