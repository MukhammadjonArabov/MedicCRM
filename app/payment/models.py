from app.users.models import BaseModel, User, Patients
from django.db import models


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Service(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='service_category')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Payments(BaseModel):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    )
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='online')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_created')
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='payments_patients')

    def __str__(self):
        return f"{self.payment_method} - {self.amount_total}"


class PaymentItems(BaseModel):
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='payment_items')

    def __str__(self):
        return f"{self.service.name} - {self.payment.amount_total}"

