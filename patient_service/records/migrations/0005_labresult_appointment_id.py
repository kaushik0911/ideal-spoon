# Generated by Django 5.1.3 on 2024-12-11 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_alter_prescription_appointment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='labresult',
            name='appointment_id',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
