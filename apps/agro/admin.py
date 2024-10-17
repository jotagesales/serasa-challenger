from django.contrib import admin
from .models import Farmer, Farm, Culture


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ['name']


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'total_area', 'vegetal_area', 'available_area', 'city', 'state')
    search_fields = ['name', 'owner']


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'document')
    search_fields = ['name', 'document']