from app.users import user_schema
from app.config import settings
from jose import jwt
import pytest


def test_root(client):
    res = client.get("/")
    assert (
        res.json().get("Message")
        == "Welcome to Diary API, where logs are saved"
    )
    assert res.status_code == 200


def test_create_user(client):
    user_in = {
        "firstname": "firstname",
        "lastname": "lastname",
        "email": "test@gmail.com",
        "password": "Password123",
        "cpassword": "Password123",
    }
    res = client.post("/account/signup", json=user_in)
    new_user = user_schema.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert new_user.firstname == "firstname"
    assert new_user.lastname == "lastname"
    assert res.status_code == 201


def test_user_login(client, test_user):
    res = client.post(
        "/login/",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    login_response = user_schema.Token(**res.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "Bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "Password123", 403),
        ("test@example.com", "wrongpassword", 403),
        ("wrongemail@example.com", "wrongpassword", 403),
        (None, "Password123", 422),
        ("test@example.com", None, 422),
    ],
)
def test_failed_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login/", data={"username": email, "password": password}
    )
    assert res.status_code == status_code
