import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Database connection details
DB_HOST = ""
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_PORT = 6543

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("Connected to the database.")
except Exception as e:
    print("Error connecting to the database:", e)
    exit()


doctors = []

# Healthcare data dictionary
healthcare_data = {
    "Cardiologist": {
        "conditions": {
            "Hypertension": {
                "medications": ["Amlodipine", "Losartan", "Metoprolol"],
                "tests": ["Blood Pressure Test", "ECG", "Echocardiogram"],
                "lab_results": ["Normal BP", "Elevated BP", "Abnormal ECG"]
            },
            "Arrhythmia": {
                "medications": ["Amiodarone", "Beta Blockers", "Calcium Channel Blockers"],
                "tests": ["Holter Monitor Test", "Electrophysiology Study"],
                "lab_results": ["Normal Rhythm", "Irregular Rhythm"]
            }
        }
    },
    "Endocrinologist": {
        "conditions": {
            "Diabetes": {
                "medications": ["Metformin", "Insulin", "Glipizide"],
                "tests": ["HbA1c", "Fasting Blood Sugar Test"],
                "lab_results": ["HbA1c < 6.5%", "HbA1c > 7%", "Normal Blood Sugar"]
            },
            "Thyroid Disorder": {
                "medications": ["Levothyroxine", "Methimazole"],
                "tests": ["TSH Test", "Free T4 Test"],
                "lab_results": ["Normal TSH", "High TSH", "Low Free T4"]
            }
        }
    }
    # Add other specialties and conditions as needed
}

def generate_random_health_data(data):
    # Select a random doctor specialty
    doctor_specialty = random.choice(list(data.keys()))
    
    # Select a random condition for the chosen specialty
    conditions = data[doctor_specialty]["conditions"]
    condition_name = random.choice(list(conditions.keys()))
    
    # Fetch details for the selected condition
    condition_details = conditions[condition_name]
    medications = random.choice(condition_details["medications"])
    test_name = random.choice(condition_details["tests"])
    lab_result = random.choice(condition_details["lab_results"])
    
    # Create a single-level dictionary
    result = {
        "doctor_id": fake.random_int(min=1, max=10000),
        "doctor_name": fake.name(),
        "specialty": doctor_specialty,
        "condition": condition_name,
        "medication": medications,
        "test_name": test_name,
        "lab_result": lab_result
    }
    
    return result


for _ in range(10):
    doctors.append(generate_random_health_data(healthcare_data))


# Generate and insert data
def insert_fake_data(cursor, num_records=10):
    for _ in range(num_records):
        doctor = random.choice(doctors)

        appointment_id = fake.random_int(min=1, max=10000)
        doctor_id = doctor["doctor_id"]
        doctor_name = doctor["doctor_name"]
        specialty = doctor["specialty"]
        patient_id = fake.random_int(min=1, max=10000)
        patient_name = fake.name()
        appointment_date = fake.date_this_month()
        start_time = fake.time()
        end_time = (datetime.strptime(start_time, "%H:%M:%S") + timedelta(minutes=30)).time()
        appointment_status = random.choice(["Scheduled", "Completed", "Cancelled", "Rescheduled"])
        medication = doctor["medication"] if random.random() > 0.5 else None
        prescribed_date = fake.date_this_month() if medication else None
        notes = fake.text(max_nb_chars=100)
        test_name = doctor["test_name"] if random.random() > 0.5 else None
        lab_result = doctor["lab_result"] if test_name else None
        date_conducted = fake.date_this_year() if lab_result else None

        # SQL Insert Query
        insert_query = """
        INSERT INTO public.appointment_details (
            appointment_id, doctor_id, doctor_name, specialty, patient_id, patient_name,
            appointment_date, start_time, end_time, appointment_status, medication, 
            prescribed_date, notes, test_name, lab_result, date_conducted
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            appointment_id, doctor_id, doctor_name, specialty, patient_id, patient_name,
            appointment_date, start_time, end_time, appointment_status, medication, 
            prescribed_date, notes, test_name, lab_result, date_conducted
        )

        cursor.execute(insert_query, values)

# Insert 100 fake records
try:
    insert_fake_data(cursor, num_records=50)
    conn.commit()
    print("Fake data inserted successfully.")
except Exception as e:
    conn.rollback()
    print("Error inserting data:", e)

# Close the connection
cursor.close()
conn.close()
print("Database connection closed.")
