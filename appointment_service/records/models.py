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
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name="appointments")
    status = models.CharField(max_length=50, default='Scheduled')

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.availability} : {self.status}"
