# Generated by Django 4.2.11 on 2024-09-03 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rol',
        ),
        migrations.DeleteModel(
            name='Rol',
        ),
    ]