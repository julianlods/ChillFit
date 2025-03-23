# Generated by Django 5.1.5 on 2025-01-15 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChillFit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rutina',
            name='bloques',
        ),
        migrations.CreateModel(
            name='Bloque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('ejercicios', models.ManyToManyField(related_name='bloques', to='ChillFit.ejercicio')),
            ],
        ),
        migrations.AddField(
            model_name='rutina',
            name='bloques',
            field=models.ManyToManyField(related_name='rutinas', to='ChillFit.bloque'),
        ),
    ]
