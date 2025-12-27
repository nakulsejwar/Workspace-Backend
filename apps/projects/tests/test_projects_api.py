import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
def test_create_project_authenticated():
    client = APIClient()

    user = User.objects.create_user(
        email="owner@example.com",
        username="owner",
        password="password123"
    )

    # Login
    login_response = client.post(
        "/api/auth/login/",
        {
            "email": "owner@example.com",
            "password": "password123"
        },
        format="json"
    )

    token = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.post(
        "/api/projects/projects/",
        {
            "name": "Test Project",
            "description": "Integration test project"
        },
        format="json"
    )

    assert response.status_code == 201
    assert response.data["name"] == "Test Project"
