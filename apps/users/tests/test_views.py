import pytest
from django.urls import reverse
from rest_framework import status


# =========================
# AUTHENTICATION TESTS
# =========================

@pytest.mark.django_db
def test_login_success(api_client, user):
    url = reverse("auth_login")
    data = {
        "email": user.email,
        "password": "12345678"
    }
    response = api_client.post(url, data=data, format="json")
    
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_fail_wrong_password(api_client, user):
    url = reverse("auth_login")
    data = {
        "email": user.email,
        "password": "wrongpassword"
    }
    response = api_client.post(url, data=data, format="json")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_login_when_already_authenticated(auth_client):
    url = reverse("auth_login")
    response = auth_client.post(url, {}, format="json")
    
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT)


@pytest.mark.django_db
def test_refresh_token(api_client, user):
    login_url = reverse("auth_login")
    login_response = api_client.post(login_url, {
        "email": user.email,
        "password": "12345678"
    }, format="json")
    
    assert login_response.status_code == status.HTTP_200_OK
    refresh_token = login_response.data["refresh"]
    
    refresh_url = reverse("auth_refresh")
    response = api_client.post(refresh_url, {"refresh": refresh_token}, format="json")
    
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_get_me(api_client, user):
    login_url = reverse("auth_login")
    login_response = api_client.post(login_url, {
        "email": user.email,
        "password": "12345678"
    }, format="json")
    
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    me_url = reverse("auth_me")
    response = api_client.get(me_url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
    assert response.data["full_name"] == user.full_name
    assert response.data["role"] == "doctor"


# =========================
# DOCTORS TESTS
# =========================

@pytest.mark.django_db
def test_doctor_list_forbidden_for_doctor(auth_client):
    url = reverse("doctor_list")
    response = auth_client.get(url)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_doctor_list_allowed_for_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse("doctor_list")
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert hasattr(response.data, "__iter__")  


# =========================
# PATIENTS TESTS (ViewSet)
# =========================

@pytest.mark.django_db
def test_patient_list(auth_client):
    url = reverse("patient-list")
    response = auth_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list) or hasattr(response.data, "__iter__")


@pytest.mark.django_db
def test_patient_create(auth_client):
    url = reverse("patient-list")
    data = {
        "full_name": "Test Patient",
        "phone_number": "+998901234999",
        "birth_date": "2000-01-01",
        "gender": "male"
    }
    response = auth_client.post(url, data, format="json")
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["full_name"] == "Test Patient"
    assert response.data["phone_number"] == "+998901234999"


@pytest.mark.django_db
def test_patient_list_contains_existing_patient(auth_client, patient):
    url = reverse("patient-list")
    response = auth_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    results = response.data
    
    full_names = [item["full_name"] for item in results]
    phone_numbers = [item["phone_number"] for item in results]
    
    assert "Ali Valiyev" in full_names
    assert "+998901112233" in phone_numbers