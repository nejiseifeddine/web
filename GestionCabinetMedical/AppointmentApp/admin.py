from django.contrib import admin

# Register your models here.
from AppointmentApp.models import Appointment
# Register your models here.


@admin.register(Appointment)
class AppointmentAdminPerso(admin.ModelAdmin):
    list_display=("id","doctor","patient","appointment_date","reason","status")
    list_filter=("doctor","patient","appointment_date","reason","status")
    search_fields=("doctor","patient","appointment_date","reason")
    
