# Generated by Django 5.1.3 on 2024-12-12 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_rename_appointment_id_prescription_lab_result_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='lab_result_id',
            new_name='prescription_id',
        ),
    ]