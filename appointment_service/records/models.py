# appointments/models.py
from django.db import models # Reference to the Patient model

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patient(models.Model):
    patient_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availabilities")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.name} - {self.date}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")

    status = models.CharField(max_length=50, default='Scheduled')

    def save(self, *args, **kwargs):
        # Automatically populate the doctor field from the availability relation
        if self.availability and self.availability.doctor:
            self.doctor = self.availability.doctor
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.availability} : {self.status}"

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="lab_results")
    test_name = models.CharField(max_length=255)
    result = models.TextField()
    date_conducted = models.DateField()
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="lab_results"
    )

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescriptions")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="prescriptions")
    medication = models.CharField(max_length=255)
    prescribed_date = models.DateField()
    notes = models.TextField()


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Prescription
from records.utils.event_publisher import publish_event

@receiver(post_save, sender=Prescription)
def prescription_saved(sender, instance, created, **kwargs):
    event_type = "PrescriptionCreated" if created else "PrescriptionUpdated"
    data = {
        "prescription_id": instance.id,
        "patient_id": instance.patient.id,
        "doctor_name": instance.doctor.name,
        "medication": instance.medication,
        "prescribed_date": instance.prescribed_date.strftime("%Y-%m-%d %H:%M:%S"),
        "notes": instance.notes
    }
    publish_event(event_type, data, "prescription_queue")

@receiver(post_delete, sender=Prescription)
def prescription_deleted(sender, instance, **kwargs):
    publish_event("PrescriptionDeleted", {"prescription_id": instance.id}, "prescription_queue")

@receiver(post_save, sender=LabResult)
def lab_result_saved(sender, instance, created, **kwargs):
    event_type = "LabResultCreated" if created else "LabResultUpdated"
    data = {
        "lab_result_id": instance.id,
        "patient_id": instance.patient.id,
        "test_name": instance.test_name,
        "result": instance.result,
        "date_conducted": instance.date_conducted.strftime("%Y-%m-%d %H:%M:%S")
    }
    publish_event(event_type, data, "lab_result_queue")

@receiver(post_delete, sender=LabResult)
def lab_result_deleted(sender, instance, **kwargs):
    publish_event("LabResultDeleted", {"lab_result_id": instance.id}, "lab_result_queue")
