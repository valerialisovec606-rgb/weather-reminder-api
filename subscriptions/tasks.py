from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.db.models import Q

from subscriptions.models import Subscription
from subscriptions.services import send_notification


@shared_task
def send_due_notifications():
    now = timezone.now()

    subscriptions = Subscription.objects.filter(
        Q(next_send_at__lte=now) | Q(next_send_at__isnull=True),
        is_active=True,
    )

    sent_count = 0

    for subscription in subscriptions:
        was_sent = send_notification(subscription)

        if was_sent:
            subscription.last_sent_at = now
            subscription.next_send_at = now + timedelta(hours=subscription.period_hours)
            subscription.save(update_fields=["last_sent_at", "next_send_at"])
            sent_count += 1

    return f"Sent {sent_count} notifications"
