from django.db import models
from locations.models import City


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    temperature = models.FloatField()
    description = models.CharField(max_length=255)

    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city.name} - {self.temperature}. {self.description}'
