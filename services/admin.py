from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'clinic')
    list_filter = ('clinic',)
    search_fields = ('name',)