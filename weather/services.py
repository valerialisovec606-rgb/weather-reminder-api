import requests
from weather.models import Weather


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self, city):
        params = {
            'id': city.provider_id,
            'appid': self.api_key,
            'units': 'metric',
        }

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise Exception(f"OpenWeather error: {response.text}")

        data = response.json()

        temperature = data['main']['temp']
        description = data['weather'][0]['description']

        weather = Weather.objects.create(
            city=city,
            temperature=temperature,
            description=description,
        )

        return weather
