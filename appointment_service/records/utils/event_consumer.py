import pika
import json
from records.models import Patient

def consume_events():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Replace 'localhost' with RabbitMQ host
    channel = connection.channel()
    channel.queue_declare(queue='patient_events')  # Declare queue if it doesn't exist

    def callback(ch, method, properties, body):
        event = json.loads(body)
        event_type = event['event']
        data = event['data']

        if event_type == "PatientCreated":
            Patient.objects.create(
                patient_id=data['patient_id'],
                name=data['name'],
                contact_number=data['contact_number']
            )
        elif event_type == "PatientUpdated":
            patient = Patient.objects.get(patient_id=data['patient_id'])
            patient.name = data['name']
            patient.contact_number = data['contact_number']
            patient.save()
        elif event_type == "PatientDeleted":
            Patient.objects.filter(patient_id=data['patient_id']).delete()

    channel.basic_consume(queue='patient_events', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
