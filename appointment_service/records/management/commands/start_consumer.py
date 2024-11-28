from django.core.management.base import BaseCommand
from records.utils.event_consumer import consume_events

class Command(BaseCommand):
    help = "Starts the RabbitMQ event consumer"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting RabbitMQ event consumer...")
        consume_events()
