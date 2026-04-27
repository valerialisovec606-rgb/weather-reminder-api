from django.test import TestCase
from django.contrib.auth import get_user_model

from locations.models import City
from .models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class SubscriptionSerializerTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name='Kyiv',
            country_code='UA',
            provider_id='703448'
        )

    def test_webhook_channel_requires_webhook_url(self):
        data = {
            'city': self.city.id,
            'period_hours': 3,
            'channel': 'webhook',
        }

        serializer = SubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('webhook_url', serializer.errors)

    def test_email_channel_does_not_require_webhook_url(self):
        data = {
            'city': self.city.id,
            'period_hours': 3,
            'channel': 'email',
        }

        serializer = SubscriptionSerializer(data=data)

        self.assertTrue(serializer.is_valid())

class SubscriptionViewSetTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )

        self.city = City.objects.create(
            name='Kyiv',
            country_code='UA',
            provider_id='703448'
        )

        Subscription.objects.create(
            user=self.user1,
            city=self.city,
            period_hours=3,
            channel='email'
        )

        Subscription.objects.create(
            user=self.user2,
            city=self.city,
            period_hours=6,
            channel='email'
        )

    def test_user_sees_only_own_subscriptions(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get('/api/subscriptions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user1.id)
