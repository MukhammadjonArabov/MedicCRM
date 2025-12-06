from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

uzbek_phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="The phone number is in the wrong format. It should be in the format +998xxxxxxxxx only."
)

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('cashier', 'Cashier'),
        ('registrar', 'Registrar'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120)
    image_user = models.ImageField(upload_to='users/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, validators=[uzbek_phone_validator])
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')
    descriptor = models.CharField(max_length=120, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Patients(BaseModel):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15, validators=[uzbek_phone_validator], unique=True)
    image_patient = models.ImageField(upload_to='patients/', null=True, blank=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    address = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"

