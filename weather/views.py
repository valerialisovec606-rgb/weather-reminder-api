from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Weather
from .serializers import WeatherSerializer
from .services import WeatherService
from locations.models import City


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False, methods=['post'])
    def update_weather(self, request):
        city_id = request.data.get('city_id')

        if not city_id:
            return Response(
                {'error': 'city_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        city = get_object_or_404(City, id=city_id)

        service = WeatherService(settings.OPENWEATHER_API_KEY)
        weather = service.get_current_weather(city)

        serializer = WeatherSerializer(weather)
        return Response(serializer.data)
