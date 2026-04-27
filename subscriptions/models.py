from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Subscription(models.Model):

    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('webhook', 'Webhook'),
    ]

    PERIOD_CHOICES = [
        (1, '1 hour'),
        (3, '3 hours'),
        (6, '6 hours'),
        (12, '12 hours'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey('locations.City', on_delete=models.CASCADE)

    period_hours = models.IntegerField(choices=PERIOD_CHOICES)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    webhook_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    next_send_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.city.name} every {self.period_hours}h'

    class Meta:
        unique_together = ['user', 'city']
