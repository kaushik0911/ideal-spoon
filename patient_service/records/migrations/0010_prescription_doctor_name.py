# Generated by Django 5.1.3 on 2024-12-12 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0009_rename_lab_result_id_prescription_prescription_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='doctor_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]