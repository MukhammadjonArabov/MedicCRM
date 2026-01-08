from django.forms import ValidationError
import pytest
from datetime import date, time
from apps.users.models import User, Patients, StaffSchedule


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email='ali@example.com',
        full_name='Ali Valiyev',
        password='password123',
        phone_number='+998902221122'
    )

    assert user.email == 'ali@example.com'
    assert user.full_name == 'Ali Valiyev'
    assert user.check_password('password123')
    assert user.phone_number == '+998902221122'
    assert user.is_active is True


@pytest.mark.django_db
def test_create_user_without_emile():
    with pytest.raises(ValueError) as excinfo:
        User.objects.create_user(
            email='',
            full_name='No Email',
            password='password123',
        )


@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(
        email="admin@gmail.com",
        full_name="Admin",
        password="adminpass123",
        phone_number="+998901112233"
    )

    assert admin.is_staff is True
    assert admin.is_superuser is True


@pytest.mark.django_db
def test_user_str_method():
    user = User.objects.create_user(
        email="str@test.com",
        full_name="String User",
        password="12345678",
        phone_number="+998901222222"
    )

    assert str(user) == "String User (str@test.com)"


@pytest.mark.django_db
def test_user_phone_validator_invalid():
    user = User(
        email="phone@test.com",
        full_name="Phone Test",
        phone_number="998901234567"  
    )

    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_create_patient():
    patient = Patients.objects.create(
        full_name="Ali Valiyev",
        phone_number="+998907777777",
        birth_date=date(1990, 1, 1),
        gender="male"
    )

    assert patient.full_name == "Ali Valiyev"
    assert patient.gender == "male"


@pytest.mark.django_db
def test_patient_str_method():
    patient = Patients.objects.create(
        full_name="Patient Test",
        phone_number="+998906666666",
        birth_date=date(2000, 5, 5),
        gender="female"
    )

    assert str(patient) == "Patient Test (+998906666666)"


@pytest.mark.django_db
def test_create_staff_schedule():
    doctor = User.objects.create_user(
        email="doctor@test.com",
        full_name="Doctor Who",
        password="12345678",
        phone_number="+998905555555",
        role="doctor"
    )

    schedule = StaffSchedule.objects.create(
        staff=doctor,
        day="Mon",
        start_time=time(9, 0),
        end_time=time(17, 0)
    )

    assert schedule.staff == doctor
    assert schedule.day == "Mon"


@pytest.mark.django_db
def test_staff_schedule_unique_together():
    nurse = User.objects.create_user(
        email="nurse@test.com",
        full_name="Nurse Joy",
        password="12345678",
        phone_number="+998904444444",
        role="nurse"
    )

    StaffSchedule.objects.create(
        staff=nurse,
        day="Tue",
        start_time=time(8, 0),
        end_time=time(16, 0)
    )

    with pytest.raises(Exception):
        StaffSchedule.objects.create(
            staff=nurse,
            day="Tue",
            start_time=time(10, 0),
            end_time=time(18, 0)
        )
