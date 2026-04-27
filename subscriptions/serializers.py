from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'city',
            'period_hours',
            'channel',
            'webhook_url',
            'is_active',
            'last_sent_at',
            'next_send_at',
        ]
        read_only_fields = ['id', 'user', 'last_sent_at', 'next_send_at']

    def validate(self, data):
        channel = data.get('channel')
        webhook_url = data.get('webhook_url')

        if channel == 'webhook' and not webhook_url:
            raise serializers.ValidationError({
                'webhook_url': 'This field is required when channel is webhook.'
            })

        return data
