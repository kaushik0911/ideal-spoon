import pika
import json
import datetime
from dotenv import load_dotenv
import os
from django.conf import settings

load_dotenv()

def publish_event(event_type, data, queue_name="default_queue"):
    # Skip publishing in test mode
    if getattr(settings, 'TESTING', False):
        print(f"Test Mode: Skipping publishing event: {event_type}")
        return

    credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), credentials=credentials)) # Replace 'localhost' with your RabbitMQ host
    channel = connection.channel()
    channel.queue_declare(queue_name)  # Declare queue if it doesn't exist

    event = {
        "event": event_type,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": data
    }
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(event)
    )
    connection.close()
