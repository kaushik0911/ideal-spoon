from django.test import TestCase
from unittest.mock import patch
from records.models import Doctor
from django.urls import reverse
from rest_framework import status

class DoctorModelTest(TestCase):

    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="John",
            specialty="Diabetes",
            contact_number="1234567890",
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.name, "John")
        self.assertEqual(self.doctor.specialty, "Diabetes")
        self.assertEqual(self.doctor.contact_number, "1234567890")

    def test_get_doctor_with_related_data(self):
        url = reverse('doctor-detail', args=[self.doctor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.doctor.name)

    def test_create_doctor(self):
        url = reverse('doctor-list')
        payload = {
            "name": "Jane",
            "contact_number": "9876543210",
            "specialty": "Diabetes"
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Jane")
