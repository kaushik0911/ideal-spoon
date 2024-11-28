import pika
import json

def publish_event(event_type, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Replace 'localhost' with your RabbitMQ host
    channel = connection.channel()
    channel.queue_declare(queue='patient_events')  # Declare queue if it doesn't exist

    event = {
        "event": event_type,
        "timestamp": "2024-11-20T12:00:00Z",
        "data": data
    }
    channel.basic_publish(
        exchange='',
        routing_key='patient_events',
        body=json.dumps(event)
    )
    connection.close()
