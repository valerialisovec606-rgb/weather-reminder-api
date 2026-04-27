from rest_framework.routers import DefaultRouter
from .views import WeatherViewSet

router = DefaultRouter()


router.register('weather', WeatherViewSet, basename='weather')

urlpatterns = router.urls