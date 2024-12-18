from django.test import TestCase
from unittest.mock import patch
from records.models import Patient, MedicalHistory, Prescription, LabResult
from django.urls import reverse
from rest_framework import status

class PatientModelTest(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            gender="Male",
            contact_number="1234567890",
            email="john.doe@example.com"
        )

    def test_patient_creation(self):
        self.assertEqual(self.patient.first_name, "John")
        self.assertEqual(self.patient.last_name, "Doe")
        self.assertEqual(self.patient.gender, "Male")
        self.assertEqual(self.patient.contact_number, "1234567890")
        self.assertEqual(self.patient.email, "john.doe@example.com")

    def test_create_patient(self):
        url = reverse('patient-list')
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1995-02-02",
            "gender": "Female",
            "contact_number": "9876543210",
            "email": "jane.doe@example.com"
        }
        response = self.client.post(url, payload)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], "Jane")

"""
    def test_get_patient_with_related_data(self):
        url = reverse('patient-detail', args=[self.patient.id])  # Assuming `router.register` is used
        response = self.client.get(url)
        print(f"hi{response}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.patient.first_name)
        self.assertEqual(len(response.data['medical_history']), 0)
        self.assertEqual(len(response.data['prescriptions']), 0)
        self.assertEqual(len(response.data['lab_results']), 0)
"""

"""
from unittest.mock import patch

class PatientSignalTestCase(TestCase):

    @patch('records.utils.event_publisher.publish_event')
    def test_patient_created_signal(self, mock_publish_event):
        patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            gender="Male",
            contact_number="1234567890",
            email="john.doe@example.com"
        )

        # Assert that `publish_event` was called with the correct arguments
        mock_publish_event.assert_called_once_with(
            "PatientCreated",
            {
                "patient_id": patient.id,
                "name": "John Doe",
                "contact_number": "1234567890"
            },
            "patient_queue"
        )
"""
