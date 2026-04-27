from unittest.mock import patch, Mock
from django.test import TestCase

from locations.models import City
from .models import Weather
from .services import WeatherService
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

class WeatherServiceTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name='Kyiv',
            country_code='UA',
            provider_id='703448'
        )

    @patch('weather.services.requests.get')
    def test_get_current_weather_creates_weather_record(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {
                'temp': 15.5
            },
            'weather': [
                {
                    'description': 'clear sky'
                }
            ]
        }

        mock_get.return_value = mock_response

        service = WeatherService(api_key='fake-api-key')
        weather = service.get_current_weather(self.city)

        self.assertEqual(Weather.objects.count(), 1)
        self.assertEqual(weather.city, self.city)
        self.assertEqual(weather.temperature, 15.5)
        self.assertEqual(weather.description, 'clear sky')

class WeatherViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.city = City.objects.create(
            name='Kyiv',
            country_code='UA',
            provider_id='703448'
        )

    @patch('weather.views.WeatherService')
    def test_update_weather_creates_weather_record(self, mock_service_class):
        self.client.force_authenticate(user=self.user)

        weather = Weather.objects.create(
            city=self.city,
            temperature=12.5,
            description='clear sky'
        )

        mock_service = mock_service_class.return_value
        mock_service.get_current_weather.return_value = weather

        response = self.client.post(
            '/api/weather/update_weather/',
            {'city_id': self.city.id},
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['city'], self.city.id)
        self.assertEqual(response.data['temperature'], 12.5)
        self.assertEqual(response.data['description'], 'clear sky')
