from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import FarmViewSet, FarmAnalyticsView

router = DefaultRouter()
router.register(r'farm', FarmViewSet, basename='farm')
urlpatterns = router.urls