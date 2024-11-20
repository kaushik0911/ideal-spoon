from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, AvailabilityViewSet, AppointmentViewSet

router = DefaultRouter()
router.register("doctors", DoctorViewSet)
router.register("availability", AvailabilityViewSet)
router.register("appointments", AppointmentViewSet)

urlpatterns = router.urls