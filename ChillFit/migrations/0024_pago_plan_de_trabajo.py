# Generated by Django 5.1.5 on 2025-03-11 02:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChillFit', '0023_remove_pago_id_pago_interno_pago_id_pago_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='plan_de_trabajo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ChillFit.plandetrabajo'),
        ),
    ]
