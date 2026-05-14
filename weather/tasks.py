from celery import shared_task
from django.conf import settings

from locations.models import City
from weather.services import WeatherService


@shared_task
def update_weather_for_all_cities():
    service = WeatherService(settings.OPENWEATHER_API_KEY)

    updated_count = 0

    for city in City.objects.all():
        service.get_current_weather(city)
        updated_count += 1

    return f"Updated weather for {updated_count} cities"