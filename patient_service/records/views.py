from rest_framework import viewsets
from .models import Patient, MedicalHistory, Prescription, LabResult
from .serializers import (
    PatientSerializer,
    MedicalHistorySerializer,
    PrescriptionSerializer,
    LabResultSerializer,
)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()[:10]
    serializer_class = PatientSerializer

class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()[:10]
    serializer_class = MedicalHistorySerializer

class PrescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Prescription.objects.all()[:10]
    serializer_class = PrescriptionSerializer

class LabResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LabResult.objects.all()[:10]
    serializer_class = LabResultSerializer
