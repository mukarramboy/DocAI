import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_view(api_client):
    url = reverse('users:register')
    payload = {"email": "viewreg@example.com", "first_name": "V", "last_name": "User", "password": "pwd1234"}

    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == 201
    assert resp.data['email'] == payload['email']
    assert User.objects.filter(email=payload['email']).exists()


@pytest.mark.django_db
def test_login_view_success(api_client, user_with_credentials):
    user, creds = user_with_credentials
    url = reverse('users:login')
    resp = api_client.post(url, creds, format='json')
    assert resp.status_code == 200
    assert 'access' in resp.data and 'refresh' in resp.data


@pytest.mark.django_db
def test_login_view_failure(api_client):
    url = reverse('users:login')
    resp = api_client.post(url, {"email": "noexist@example.com", "password": "bad"}, format='json')
    assert resp.status_code == 401
    assert 'error' in resp.data
