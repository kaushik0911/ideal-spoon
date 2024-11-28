from rest_framework import serializers
from .models import Doctor, Patient, Availability, Appointment

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(many=True, read_only=True)  # Display doctor name instead of ID

    class Meta:
        model = Availability
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()  # Display patient name
    doctor = serializers.StringRelatedField()  # Display doctor name
    availability = serializers.StringRelatedField()  # Display availability details

    class Meta:
        model = Appointment
        fields = '__all__'
