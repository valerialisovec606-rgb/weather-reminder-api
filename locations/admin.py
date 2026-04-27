from django.contrib import admin
from .models import City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country_code', 'provider_id')
    search_fields = ('name', 'country_code', 'provider_id')
    ordering = ('name',)
