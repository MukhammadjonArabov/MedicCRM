import pytest
from datetime import date, time
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


@pytest.mark.django_db
def test_user_list_retrieve_serializer():
    user = User.objects.create_user(
        email="user@gmail.com",
        full_name="Sobir Olimov",
        password="123456789",
        phone_number="+998951234567"
    )
    serializer = UserListRetrieveSerializer(user)
    assert serializer.data['email'] == "user@gmail.com"
    assert "password" not in serializer.data


@pytest.mark.django_db
def test_staff_schedule_serializer():
    staff = User.objects.create_user(
        email="ali@gmail.com",
        full_name="Doctor Ali",
        password="312356751",
        phone_number="+998955551122",
        role="doctor"
    )

    schedule = StaffSchedule.objects.create(
        staff=staff,
        day="Mon",
        start_time=time(9, 0),
        end_time=time(17, 0),
    )

    serializer = StaffScheduleSerializer(schedule)
    assert serializer.data['staff_name'] == "Doctor Ali"
    assert serializer.data['day_display'] == "Monday"


@pytest.mark.django_db
def test_staff_schedule_create_serializer_valid():
    staff = User.objects.create_user(
        email="sobir@gmail.com",
        full_name="Sobir Olimov",
        password="1235689098",
        phone_number="+998977777777",
        role="nurse"
    )

    data = {
        "staff": staff.id,
        "day": "Tue",
        "start_time": "09:00",
        "end_time": "17:00",
    }

    serializer = StaffScheduleCreateSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_staff_schedule_create_serializer_invalid_item():
    staff = User.objects.create_user(
        email="karim@gmail.com",
        full_name="Karim Botiraliyev",
        password="957986y94h895",
        phone_number="+998955551199",
        role="doctor"
    )

    data = {
        "staff": staff.id,
        "day": "Wed",
        "start_time": "18:00",
        "end_time": "09:00",
    }

    serializer = StaffScheduleCreateSerializer(data=data)
    with pytest.raises(DRFValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_patient_list_serializer():
    patients = Patients.objects.create(
        full_name="Abbos Rashidov",
        phone_number="+998955554433",
        birth_date=date(2000, 1, 1),
        gender="male"
    )

    serializer = PatientListSerializer(patients)
    assert serializer.data['full_name'] == "Abbos Rashidov"


@pytest.mark.django_db
def test_patient_detail_serializer():
    patient = Patients.objects.create(
        full_name="Akbar Soliyev",
        phone_number="+998955554477",
        birth_date=date(2004, 1, 13),
        gender="female",
        address="Namangan Viloyati Chust tumani",
        notes="Bo'g'inaltrda shamollash",
    )

    serializer = PatientDetailSerializer(patient)

    assert serializer.data["address"] == "Namangan Viloyati Chust tumani"
    assert serializer.data["notes"] == "Bo'g'inaltrda shamollash"


@pytest.mark.django_db
def test_patient_create_update_serializer():
    data = {
        "full_name": "Ahat Shomirodov",
        "phone_number": "+998955550099",
        "birth_date": "2003-01-01",
        "gender": "male",
        "address": "Toshekt Viloyati Olmazor tumani",
        "notes": "Bo'g'inaltrda shamollash",
    }

    serializer = PatientCreateUpdateSerializer(data=data)

    assert serializer.is_valid()
    patient = serializer.save()

    assert patient.full_name == "Ahat Shomirodov"
