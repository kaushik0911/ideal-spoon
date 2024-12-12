import pika
import psycopg2
import json

from dotenv import load_dotenv
import os
load_dotenv()

# Database connection settings
DB_CONFIG = {
    "dbname": "postgres",
    "user": os.getenv('DBUSER'),
    "password": os.getenv('DBPASSWORD'),
    "host": os.getenv('DBHOST'),
    "port": os.getenv('DBPORT'),
}

# RabbitMQ settings
QUEUE_NAME = "prescription_queue"

# Connect to the database
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Process lab results update message
def process_message(ch, method, properties, body):
    print("Received message:", body)
    try:
        data = json.loads(body)['data']

        prescription_id = data["prescription_id"]
        patient_id = data["patient_id"]
        doctor_name = data["doctor_name"]
        medication = data["medication"]
        prescribed_date = data["prescribed_date"]
        notes = data["notes"]

        # Update patient in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO records_prescription (prescription_id, patient_id, doctor_name, medication, prescribed_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (prescription_id)
            DO UPDATE SET patient_id = EXCLUDED.patient_id, doctor_name = EXCLUDED.doctor_name, medication = EXCLUDED.medication, prescribed_date = EXCLUDED.prescribed_date, notes = EXCLUDED.notes;
        """

        cursor.execute(query, (prescription_id, patient_id, doctor_name, medication, prescribed_date, notes))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Prescription {prescription_id} updated successfully.")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

# Main consumer logic
def start_consumer():
    credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST', 'localhost'), credentials=credentials)) 
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    print(f"Waiting for messages in queue: {QUEUE_NAME}")
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)
    channel.start_consuming()

if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        print("Consumer stopped.")
