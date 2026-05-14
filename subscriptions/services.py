import requests

from django.conf import settings
from django.core.mail import send_mail

from weather.models import Weather


def get_latest_weather_for_subscription(subscription):
    return (
        Weather.objects
        .filter(city=subscription.city)
        .order_by("-recorded_at")
        .first()
    )

def build_weather_message(subscription, weather):
    message = f'Weather in {subscription.city.name}: {weather.temperature}°C, {weather.description}'
    return message

def send_email_notification(subscription, weather):
    if not subscription.user.email:
        return False

    message = build_weather_message(subscription, weather)

    send_mail(
        subject=f'Weather notification: {subscription.city.name}',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscription.user.email],
        fail_silently=False,
    )

    return True

def send_webhook_notification(subscription, weather):
    if not subscription.webhook_url:
        return False

    payload = {
        'city': subscription.city.name,
        'country_code': subscription.city.country_code,
        'temperature': weather.temperature,
        'description': weather.description,
        'recorded_at': weather.recorded_at.isoformat(),
    }

    response = requests.post(
        subscription.webhook_url,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return True

def send_notification(subscription):
    weather = get_latest_weather_for_subscription(subscription)

    if weather is None:
        return False

    if subscription.channel == 'email':
        return send_email_notification(subscription, weather)

    if subscription.channel == 'webhook':
        return send_webhook_notification(subscription, weather)

    return False
