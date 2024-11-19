from locust import HttpUser, task, between
from faker import Faker

fake = Faker()

class PatientServiceUser(HttpUser):
    host = "http://127.0.0.1:8000" 
    wait_time = between(1, 5)

    @task(3)
    def create_patient(self):
        self.client.post("/api/patients/", json={
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": str(fake.date_of_birth()),
            "gender": fake.random_element(["Male", "Female"]),
            "contact_number": fake.phone_number(),
            "email": fake.email()
        })

    @task(1)  # Weight of 1
    def list_patients(self):
        self.client.get("/api/patients/")

    @task(2)  # Weight of 2
    def get_patient_details(self):
        # Assuming ID 1 exists for testing purposes
        self.client.get("/api/patients/1/")
