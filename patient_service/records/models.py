from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_history')
    condition = models.CharField(max_length=255)
    diagnosis_date = models.DateField()
    notes = models.TextField()

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    prescribed_date = models.DateField()
    notes = models.TextField()

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=255)
    result = models.TextField()
    date_conducted = models.DateField()


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Patient
from records.utils.event_publisher import publish_event

@receiver(post_save, sender=Patient)
def patient_saved(sender, instance, created, **kwargs):
    event_type = "PatientCreated" if created else "PatientUpdated"
    data = {
        "patient_id": instance.id,
        "name": f"{instance.first_name} {instance.last_name}",
        "contact_number": instance.contact_number
    }
    publish_event(event_type, data)

@receiver(post_delete, sender=Patient)
def patient_deleted(sender, instance, **kwargs):
    publish_event("PatientDeleted", {"patient_id": instance.id})
