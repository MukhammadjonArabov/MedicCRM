import pytest
from datetime import date, time
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.users.models import User, StaffSchedule, Patients
from apps.users.serializers import (
    LoginSerializer, TokenResponseSerializer, RefreshTokenSerializer, UserSerializer, UserListRetrieveSerializer, 
    StaffScheduleSerializer, StaffScheduleCreateSerializer, PatientListSerializer, 
    PatientDetailSerializer, PatientCreateUpdateSerializer,
)

def test_login_serializer_valid():
    data = {
        "email": "test@gmail.com",
        "password": "12345678"
    }
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["email"] == data["email"]
    assert serializer.validated_data["password"] == data["password"]


def test_token_response_serializer_user_field():
    serializer = TokenResponseSerializer()
    user_data = serializer.get_user(obj=None)

    assert "id" in user_data
    assert "email" in user_data
    assert "full_name" in user_data
    assert "role" in user_data


def test_refresh_token_serializer_valid():
    serializer = RefreshTokenSerializer(data={"refresh": "fake-refresh-token"})
    assert serializer.is_valid()


@pytest.mark.django_db
def test_user_serializer_create():
    data = {
        "email": "test@gmail.com",
        "password": "123456789",
        "full_name": "Jon Roy",
        "role": "admin",
        "phone_number": "+998951234567"
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == "test@gmail.com"
    assert user.check_password("123456789")
    assert user.is_staff is True


@pytest.mark.django_db
def test_user_serializer_password_required():
    data = {
        "email": "test@gmail.com",
        "full_name": "Jon Roy",
        "role": "doctor",
        "phone_number": "+998951234567"
    }
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors


@pytest.mark.django_db
def test_user_serializer_update():
    user = User.objects.create_user(
        email="test@gmail.com",
        full_name="Old Name",
        password="123456789",
        phone_number="+998951234567"
    )

    serializer = UserSerializer(
        instance=user,
        data={"full_name": "New Name"},
        partial=True
    )
    assert serializer.is_valid()
    user = serializer.save()
    assert user.full_name == "New Name"

    





