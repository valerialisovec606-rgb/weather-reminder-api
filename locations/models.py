from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class City(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    provider_id = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.country_code}'

    class Meta:
        unique_together = ['name', 'country_code']

