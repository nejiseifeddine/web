from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("La date de naissance doit être < date d'aujord'hui")

length_validation = RegexValidator(
    regex=r'^\d{8}$',
    message="Ce champ doit contenir exactement 8 chiffres.",
)

class User(AbstractUser):
    pass

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ['name']

    def __str__(self):
        return self.name

class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)],
        verbose_name="Numéro d'inscription à l'ordre",
    )
    specialties = models.ManyToManyField(
        Specialty,
        related_name='doctors',
        blank=True,
    )
    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"

    def __str__(self):
        return f"Dr {self.first_name} {self.last_name}".strip()


class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[length_validation],
        verbose_name="CIN",
    )
    phone = models.CharField(
        max_length=8,
        validators=[length_validation],
        verbose_name="Téléphone",
    )
    birth_date = models.DateField(
        validators=[validate_past_date],  
        verbose_name="Date de naissance",
    )
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date >= timezone.localdate():
            raise ValidationError(
                {'birth_date': "La date de naissance doit être < date d'aujord'hui."}
            )

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()