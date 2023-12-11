# Generated by Django 4.2.7 on 2023-11-24 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_room_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='bills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('title', models.CharField(max_length=30)),
                ('due', models.DateTimeField(null=True)),
                ('assigned', models.DateField(auto_now=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.room')),
            ],
        ),
    ]
