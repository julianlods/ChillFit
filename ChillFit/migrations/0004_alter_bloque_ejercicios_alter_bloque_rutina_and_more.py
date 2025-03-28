# Generated by Django 5.1.5 on 2025-01-15 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChillFit', '0003_bloque_duracion_bloque_rutina_remove_rutina_bloques_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloque',
            name='ejercicios',
            field=models.ManyToManyField(blank=True, related_name='bloques', to='ChillFit.ejercicio'),
        ),
        migrations.AlterField(
            model_name='bloque',
            name='rutina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bloques_de_rutina', to='ChillFit.rutina'),
        ),
        migrations.RemoveField(
            model_name='rutina',
            name='bloques',
        ),
        migrations.AddField(
            model_name='rutina',
            name='bloques',
            field=models.ManyToManyField(blank=True, related_name='rutinas', to='ChillFit.bloque'),
        ),
    ]
