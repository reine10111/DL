# Generated by Django 4.2.7 on 2023-11-26 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_submission_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='bills',
            name='remarks',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
