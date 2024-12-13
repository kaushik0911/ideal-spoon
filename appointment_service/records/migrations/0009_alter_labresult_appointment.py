# Generated by Django 5.1.3 on 2024-12-12 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_remove_appointment_lab_result_labresult_appointment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labresult',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lab_results', to='records.appointment'),
        ),
    ]