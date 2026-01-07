import pytest
from types import SimpleNamespace
from apps.users.permissions import (
    IsDoctor, IsAdmin, IsDoctorOrAdminOrRegisterOrNurse,
    IsDoctorOrAdminOrRegistrar, IsAdminOrRegistrar, IsDoctorOrAdmin
)


def get_request(user):
    return SimpleNamespace(user=user)


@pytest.fixture
def doctor_user():
    return SimpleNamespace(
        is_authenticated=True,
        role='doctor',
    )


@pytest.fixture
def admin_user():
    return SimpleNamespace(
        is_authenticated=True,
        role='admin',
    )


@pytest.fixture
def nurse_user():
    return SimpleNamespace(
        is_authenticated=True,
        role='nurse',
    )


@pytest.fixture
def register_user():
    return SimpleNamespace(
        is_authenticated=True,
        role='register',
    )


@pytest.fixture
def anonymous_user():
    return SimpleNamespace(
        is_authenticated=False,
        role=None
    )


def test_is_doctor_permission(doctor_user):
    permission = IsDoctor()
    request = get_request(doctor_user)
    assert permission.has_permission(request, None) is True


def test_is_doctor_permission_denied_for_admin(admin_user):
    permission = IsDoctor()
    request = get_request(admin_user)
    assert permission.has_permission(request, None) is False


def test_id_admin_permission(admin_user):
    permission = IsAdmin()
    request = get_request(admin_user)
    assert permission.has_permission(request, None) is True


def test_is_admin_permission_denied_for_doctor(doctor_user):
    permission = IsAdmin()
    request = get_request(doctor_user)
    assert permission.has_permission(request, None) is False


def test_is_doctor_or_admin_or_registrar_or_nurse():
    permission = IsDoctorOrAdminOrRegisterOrNurse()

    for role in ['doctor', 'admin', 'nurse', 'registrar']:
        user = SimpleNamespace(is_authenticated=True, role=role)
        request = get_request(user)
        assert permission.has_permission(request, None) is True


def test_is_doctor_or_admin_or_registrar_denied_for_nurse(nurse_user):
    permission = IsDoctorOrAdminOrRegistrar()
    request = get_request(nurse_user)
    assert permission.has_permission(request, None) is False


def test_is_admin_or_registrar_allowed():
    permission = IsAdminOrRegistrar()
    for role in ['admin', 'registrar']:
        user = SimpleNamespace(is_authenticated=True, role=role)
        request = get_request(user)
        assert permission.has_permission(request, None) is True


def test_is_admin_or_register_denied_for_doctor(doctor_user):
    permission = IsAdminOrRegistrar()
    request = get_request(doctor_user)
    assert permission.has_permission(request, None) is False


def test_is_doctor_or_admin_allowed(doctor_user, admin_user):
    permission = IsDoctorOrAdmin()
    assert permission.has_permission(get_request(doctor_user), None) is True
    assert permission.has_permission(get_request(admin_user), None) is True


def test_is_doctor_or_admin_denied_for_anonymous(anonymous_user):
    permission = IsDoctorOrAdmin()
    request = get_request(anonymous_user)
    assert permission.has_permission(request, None) is False
















