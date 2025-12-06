from app.users.models import BaseModel, User, Patients
from django.db import models


class Queue(BaseModel):
    QUEUE_CHOICES = (
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'},
        related_name='queues_doctor',
        )
    patient = models.ForeignKey(
        Patients,
        on_delete=models.CASCADE,
        related_name='queues_patient',
    )
    status = models.CharField(max_length=20, choices=QUEUE_CHOICES, default='waiting')

    def __str__(self):
        return f'{self.patient} - {self.doctor}'

class Meeting(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(
        Patients,
        on_delete=models.CASCADE,
        related_name='meetings_patient'
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meetings_doctor',
        limit_choices_to={'role': 'doctor'}
    )
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='meetings_created',
    )

    def __str__(self):
        return f'{self.patient} - {self.doctor}'