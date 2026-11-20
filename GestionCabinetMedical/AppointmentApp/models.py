from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    appointment_date = models.DateTimeField(verbose_name="Date du rendez-vous")
    reason = models.TextField(verbose_name="Motif")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="Ordonnance",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments',
    )
    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
    )

    
    def clean(self):
        super().clean()
        if not self.appointment_date:
            return

       
        date_changed = True
        if self.pk:
            old_date = (
                Appointment.objects.filter(pk=self.pk)
                .values_list('appointment_date', flat=True)
                .first()
            )
            date_changed = old_date != self.appointment_date

        if date_changed and self.appointment_date <= timezone.now():
            raise ValidationError(
                {'appointment_date': "La date du rendez-vous doit être > date d'aujord'hui."}
            )

    def __str__(self):
        return f"{self.patient} — {self.doctor} — {self.appointment_date:%d/%m/%Y %H:%M}"
