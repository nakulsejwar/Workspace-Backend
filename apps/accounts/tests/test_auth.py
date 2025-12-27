import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
def test_user_login_with_email():
    client = APIClient()

    # Create test user
    User.objects.create_user(
        email="testuser@example.com",
        username="testuser",
        password="password123"
    )

    response = client.post(
        "/api/auth/login/",
        {
            "email": "testuser@example.com",
            "password": "password123"
        },
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
