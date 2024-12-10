import pika
import psycopg2
import json

from dotenv import load_dotenv
import os
load_dotenv()

# Database connection settings
DB_CONFIG = {
    "dbname": os.getenv('DBNAME'),
    "user": os.getenv('DBUSER'),
    "password": os.getenv('DBPASSWORD'),
    "host": os.getenv('DBHOST'),
    "port": os.getenv('DBPORT'),
}

# RabbitMQ settings
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "patient_updates"
SCHEMA = os.getenv('DBSCHEMA')

# Connect to the database
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Process patient update message
def process_message(ch, method, properties, body):
    print("Received message:", body)
    try:
        data = json.loads(body)
        patient_id = data["patient_id"]
        name = data["name"]
        contact_number = data["contact_number"]

        # Update patient in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO {%s} (patient_id, name, contact_number)
            VALUES (%s, %s, %s)
            ON CONFLICT (patient_id)
            DO UPDATE SET name = EXCLUDED.name, contact_number = EXCLUDED.contact_number;
        """
        cursor.execute(query, (SCHEMA, patient_id, name, contact_number))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Patient {patient_id} updated successfully.")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

# Main consumer logic
def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
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
