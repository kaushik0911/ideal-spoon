from rest_framework import viewsets
from .models import Doctor, Patient, Availability, Appointment
from .serializers import DoctorSerializer, PatientSerializer, AvailabilitySerializer, AppointmentReadSerializer, AppointmentWriteSerializer
from django_filters.rest_framework import DjangoFilterBackend

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient_id', 'name']

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AppointmentWriteSerializer
        return AppointmentReadSerializer
