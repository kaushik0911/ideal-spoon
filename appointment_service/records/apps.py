from django.apps import AppConfig
from django.db import connection

class RecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'records'

    def ready(self):
        # This will run when the app is ready
        with connection.cursor() as cursor:
            cursor.execute('SET search_path TO appointment_service')
