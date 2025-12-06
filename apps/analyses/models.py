from apps.users.models import BaseModel, User, Patients
from django.db import models

class Analyses(BaseModel):
    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
    )

    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='analyses_patient')
    analysis_type = models.CharField(max_length=120)
    results = models.JSONField(null=True, blank=True)
    file = models.FileField(upload_to='analyses/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return f"{self.patient.full_name} ({self.patient.phone_number})"

class Prescriptions(BaseModel):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='prescriptions_patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'},
                               related_name='prescriptions')
    medicines = models.JSONField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient.full_name} ({self.patient.phone_number})"

class AuditLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    entity = models.CharField(max_length=100)
    entity_id = models.UUIDField()

    def __str__(self):
        return f"{self.action} ({self.entity})"

class MedicalRecords(BaseModel):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='medical_records_patient')
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='medical_records_doctor', limit_choices_to={'role': 'doctor'}
    )
    diagnosis = models.TextField()
    treatment = models.TextField()
    recommendations = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient.full_name} ({self.patient.phone_number})"