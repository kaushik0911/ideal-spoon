from rest_framework import serializers
from .models import Doctor, Patient, Availability, Appointment, Prescription, LabResult

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class LabResultReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'

class AppointmentReadSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    availability = AvailabilitySerializer()
    prescription = serializers.PrimaryKeyRelatedField(read_only=True)  # Include appointment details if needed
    lab_results = LabResultReadSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

class LabResultSerializer(serializers.ModelSerializer):
    lab_result = AppointmentReadSerializer(allow_null=True, required=False)

    class Meta:
        model = LabResult
        fields = '__all__'

class AppointmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = '__all__'
        extra_kwargs = {
            'doctor': {'read_only': True},  # Exclude doctor from being set via API
        }

class PrescriptionReadSerializer(serializers.ModelSerializer):
    appointment = AppointmentReadSerializer()
    class Meta:
        model = Prescription
        fields = '__all__'

class PrescriptionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

