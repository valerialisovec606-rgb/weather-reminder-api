from django.contrib import admin
from .models import Weather


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('recorded_at', 'city', 'temperature', 'description')
    list_filter = ('recorded_at', 'city')
    search_fields = ('city__name', 'description')
