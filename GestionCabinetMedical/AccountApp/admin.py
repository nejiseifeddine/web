from django.contrib import admin
from AccountApp.models import User,Doctor,Patient,Specialty
# Register your models here.

@admin.register(User)
class UserPerso(admin.ModelAdmin):
   pass

@admin.register(Doctor)
class DoctorPerso(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "license_number", "get_specialties")

    def get_specialties(self, obj):
        return ", ".join([s.name for s in obj.specialties.all()])

    get_specialties.short_description = "Specialties"

@admin.register(Patient)
class PatientPerso(admin.ModelAdmin):
    list_display=("id","first_name","last_name","national_id","phone","birth_date")
    
admin.site.register(Specialty)