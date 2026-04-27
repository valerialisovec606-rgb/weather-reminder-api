from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'period_hours', 'next_send_at', 'is_active')
    list_filter = ('channel', 'period_hours', 'is_active', 'city')
    search_fields = ('user__username', 'city__name')
