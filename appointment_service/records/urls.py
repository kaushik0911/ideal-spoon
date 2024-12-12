from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, PatientViewSet, AvailabilityViewSet, AppointmentViewSet, LabResultViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'lab_results', LabResultViewSet)

urlpatterns = router.urls