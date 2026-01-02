import pytest
from datetime import date
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


    