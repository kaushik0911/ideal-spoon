# Generated by Django 5.1.3 on 2024-12-12 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_labresult_appointment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labresult',
            name='appointment_id',
        ),
    ]
