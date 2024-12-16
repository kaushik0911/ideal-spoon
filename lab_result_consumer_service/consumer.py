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
QUEUE_NAME = "lab_result_queue"

# Connect to the database
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Process lab results update message
def process_message(ch, method, properties, body):
    print("Received message:", body)
    try:
        data = json.loads(body)['data']

        lab_result_id= data["lab_result_id"]
        patient_id= data["patient_id"]
        test_name= data["test_name"]
        result= data["result"]
        date_conducted= data["date_conducted"]

        # Update patient in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO records_labresult (lab_result_id, patient_id, test_name, result, date_conducted)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (lab_result_id)
            DO UPDATE SET patient_id = EXCLUDED.patient_id, test_name = EXCLUDED.test_name, result = EXCLUDED.result, date_conducted = EXCLUDED.date_conducted;
        """

        cursor.execute(query, (lab_result_id, patient_id, test_name, result, date_conducted))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"LabResults {patient_id} updated successfully.")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

# Main consumer logic
def start_consumer():
    credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), credentials=credentials)) 
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
