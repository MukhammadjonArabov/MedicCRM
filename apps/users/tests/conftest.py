import pytest
from datetime import date
from rest_framework.test import APIClient
from apps.users.models import User, Patients

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@example.com",
        full_name="Test User",
        password="12345678",
        phone_number="+998901234567",
        role="doctor"
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@example.com",
        full_name="Admin User",
        password="admin123",
        phone_number="+998909999999"
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def patient(db):
    return Patients.objects.create(
        full_name="Ali Valiyev",
        phone_number="+998901112233",
        birth_date=date(1995, 5, 20),
        gender="male"
    )