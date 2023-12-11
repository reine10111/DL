# Generated by Django 4.2.7 on 2023-12-01 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_task_delete_group_contribution'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.room')),
            ],
            options={
                'db_table': 'tblevents',
            },
        ),
    ]