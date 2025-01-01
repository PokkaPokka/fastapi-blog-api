import os
from app import schemas
import pytest
from jose import jwt


def test_create_user_invalid_password(client):
    response = client.post(
        "/users/",
        json={
            "email": "test2.create.user@gmail.com",
            "password": "password",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number"
    }


def test_create_user_invalid_email(client):
    response = client.post(
        "/users/",
        json={
            "email": "invalid-email-format",
            "password": "testPassword1",
        },
    )
    assert response.status_code == 422


def test_create_user_duplicate_email(client, test_user):
    response = client.post(
        "/users/",
        json={
            "email": "test1.create.user@gmail.com",
            "password": "testPassword1",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": f"User with email: {test_user['email']} already exists."
    }


def test_login(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_response = schemas.Token(**response.json())

    payload = jwt.decode(
        login_response.access_token,
        os.getenv("OAUTH_SECRET_KEY"),
        algorithms=os.getenv("ALGORITHM"),
    )
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrong.email@gmail.com", "testPassword1", 403),
        ("test1.create.user@gmail.com", "wrong_password", 403),
        ("hahaha@gmail.com", "hahaha", 403),
        (None, "testPassword1", 422),
        ("test1.create.user@gmail.com", None, 422),
        ("", "testPassword1", 422),
        ("test1.create.user@gmail.com", "", 422),
        ("invalid-email-format", "testPassword1", 403),
        ("TEST1.CREATE.USER@GMAIL.COM", "testPassword1", 403),  # Case sensitivity check
        ("test1.create.user@gmail.com", "TESTPASSWORD1", 403),  # Case sensitivity check
        ("' OR '1'='1", "testPassword1", 403),  # SQL injection attempt
        ("test1.create.user@gmail.com", "' OR '1'='1", 403),  # SQL injection attempt
    ],
)
def test_login_invalid_password(client, email, password, status_code):
    response = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == status_code
