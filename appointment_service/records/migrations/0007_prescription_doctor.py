# Generated by Django 5.1.3 on 2024-12-12 06:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_remove_labresult_appointment_appointment_lab_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='records.doctor'),
            preserve_default=False,
        ),
    ]