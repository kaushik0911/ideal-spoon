import pika
import json
import datetime

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "patient_events"

def publish_event(event_type, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))  # Replace 'localhost' with your RabbitMQ host
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)  # Declare queue if it doesn't exist

    event = {
        "event": event_type,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": data
    }
    channel.basic_publish(
        exchange='',
        routing_key='patient_events',
        body=json.dumps(event)
    )
    connection.close()
