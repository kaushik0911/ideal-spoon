from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, MedicalHistoryViewSet, PrescriptionViewSet, LabResultViewSet

router = DefaultRouter()
router.register('patients', PatientViewSet)
router.register('medical-history', MedicalHistoryViewSet)
router.register('prescriptions', PrescriptionViewSet)
router.register('lab-results', LabResultViewSet)

urlpatterns = router.urls
