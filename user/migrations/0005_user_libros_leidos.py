# Generated by Django 4.2.11 on 2024-09-27 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_libro_imgportada'),
        ('user', '0004_user_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='libros_leidos',
            field=models.ManyToManyField(blank=True, related_name='usuarios_que_leyeron', to='myapp.libro'),
        ),
    ]
