# Generated by Django 5.1.5 on 2025-03-11 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChillFit', '0020_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='pagado',
        ),
        migrations.AddField(
            model_name='pago',
            name='descripcion',
            field=models.CharField(default='Pago del mes', help_text="Ejemplo: 'Clase 1' o 'Mensualidad Enero'", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pago',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], default='pendiente', max_length=10),
        ),
    ]
