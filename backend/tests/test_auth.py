import time
import pytest


def test_routes(client):
    """This test prints out all available API routes."""
    print("Printing API routes...")
    for route in client.app.routes:
        print(route.path)


@pytest.fixture
def registered_user(client):
    base_registered_user_email = "test@example.com"
    base_registered_user_password = "mypassword123"
    response = client.post(
        "/api/auth/register",
        json={
            "email": base_registered_user_email,
            "password": base_registered_user_password,
        },
    )
    yield {
        "response": response,
        "email": base_registered_user_email,
        "password": base_registered_user_password,
    }


@pytest.fixture
def registered_web_user(client):
    base_registered_user_email = "test@example.com"
    base_registered_user_password = "mypassword123"
    response = client.post(
        "/api/auth/register-web",
        json={
            "email": base_registered_user_email,
            "password": base_registered_user_password,
        },
    )
    yield {
        "response": response,
        "email": base_registered_user_email,
        "password": base_registered_user_password,
    }


def test_register_web_success(client, registered_web_user):
    response = registered_web_user["response"]
    assert response.status_code == 201
    assert "access_token" not in response.json()
    assert "Set-Cookie" in response.headers
    assert "access_token" in response.cookies


def test_register_success(client, registered_user):
    response = registered_user["response"]
    assert response.status_code == 201
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_register_duplicate_email(client, registered_user):
    user_email = registered_user["email"]
    user_password = registered_user["password"]

    # Try again with same email
    response = client.post(
        "/api/auth/register",
        json={"email": user_email, "password": user_password},
    )
    assert response.status_code == 400


def test_login_success(client, registered_user):
    user_email = registered_user["email"]
    user_password = registered_user["password"]

    # Then login
    response = client.post(
        "/api/auth/login",
        json={"email": user_email, "password": user_password},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client, registered_user):
    user_email = registered_user["email"]

    response = client.post(
        "/api/auth/login",
        json={"email": user_email, "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_missing_email(client):
    response = client.post("/api/auth/login", json={"password": "mypassword123"})
    assert response.status_code == 422  # Pydantic catches this


def test_access_rotation(client, registered_user):
    register_response = registered_user["response"]
    register_response_json = register_response.json()

    access_token = register_response_json.get("access_token", "")

    refresh_response = client.post(
        "/api/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()
    assert refresh_response.json()["token_type"] == "bearer"
    assert (
        refresh_response.json()["access_token"]
        != register_response.json()["access_token"]
    )


def test_access_rotation_web(client, registered_web_user):
    register_response = registered_web_user["response"]

    refresh_response = client.post(
        "/api/auth/refresh-web",
        cookies={"access_token": register_response.cookies["access_token"]},
    )

    assert refresh_response.status_code == 200
    assert "access_token" not in refresh_response.json()
    assert "access_token" in refresh_response.cookies
    assert (
        refresh_response.cookies["access_token"]
        != register_response.cookies["access_token"]
    )


@pytest.fixture
def test_getting_public_id(client, registered_user):
    register_response = registered_user["response"]
    register_response_json = register_response.json()

    access_token = register_response_json.get("access_token", "")

    sessions_info_response = client.post(
        "/api/auth/sessions-info",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert sessions_info_response.status_code == 200
    assert "sessions" in sessions_info_response.json()

    return {
        "session_info_json": sessions_info_response.json(),
        "register_response_json": register_response_json,
    }


def test_revocation(client, test_getting_public_id):
    sessions_info_response_json = test_getting_public_id["session_info_json"]
    register_response_json = test_getting_public_id["register_response_json"]

    assert len(sessions_info_response_json.get("sessions", [])) > 0
    session_id = sessions_info_response_json.get("sessions")[0].get("session_id", "")

    access_token = register_response_json.get("access_token", "")

    revoke_response = client.post(
        "/api/auth/revoke-sessions",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"ids_to_revoke": [session_id]},
    )

    assert revoke_response.status_code == 200
    assert revoke_response.json().get("revoked_ids", ["null"])[0] == session_id

    should_be_revoked_access_token = register_response_json.get("access_token", "")

    me_response_should_fail = client.get(
        "/api/me/info",
        headers={"Authorization": f"Bearer {should_be_revoked_access_token}"},
    )

    assert me_response_should_fail.status_code == 401


@pytest.fixture
def test_getting_public_id_web(client, registered_web_user):
    register_response = registered_web_user["response"]
    access_token_cookie = register_response.cookies["access_token"]

    sessions_info_response = client.post(
        "/api/auth/sessions-info",
        cookies={"access_token": access_token_cookie},
    )

    assert sessions_info_response.status_code == 200
    assert "sessions" in sessions_info_response.json()

    return {
        "session_info_json": sessions_info_response.json(),
        "register_response_cookie": access_token_cookie,
    }


def test_revocation_web(client, test_getting_public_id_web):
    sessions_info_response_json = test_getting_public_id_web["session_info_json"]
    access_token_cookie = test_getting_public_id_web["register_response_cookie"]

    assert len(sessions_info_response_json.get("sessions", [])) > 0
    session_id = sessions_info_response_json.get("sessions")[0].get("session_id", "")

    revoke_response = client.post(
        "/api/auth/revoke-sessions",
        cookies={"access_token": access_token_cookie},
        json={"ids_to_revoke": [session_id]},
    )

    assert revoke_response.status_code == 200
    assert revoke_response.json().get("revoked_ids", ["null"])[0] == session_id

    me_response_should_fail = client.get(
        "/api/me/info",
        cookies={"access_token": access_token_cookie},
    )

    assert me_response_should_fail.status_code == 401


def test_access_expiration(client, monkeypatch):
    monkeypatch.setattr("app.core.config.settings.access_token_expire_minutes", 0)

    register_response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "mypassword123"},
    )
    assert register_response.status_code == 201

    access_token = register_response.json()["access_token"]

    time.sleep(1)

    expired_token_response = client.get(
        "/api/me/info",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert expired_token_response.status_code == 401

    monkeypatch.setattr("app.core.config.settings.access_token_expire_minutes", 1)

    time.sleep(1)

    login_response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "mypassword123"},
    )
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    third_response = client.post(
        "/api/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert third_response.status_code == 200

    access_token = third_response.json()["access_token"]

    time.sleep(1)

    fourth_response = client.get(
        "/api/me/info",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert fourth_response.status_code == 200


@pytest.fixture
def making_temp_web(client):
    register_response = client.post("/api/auth/temp-credentials-web")
    assert register_response.status_code == 201

    access_token_cookie = register_response.cookies["access_token"]

    info_response = client.post(
        "/api/auth/sessions-info",
        cookies={"access_token": access_token_cookie},
    )

    assert info_response.status_code == 200
    assert info_response.json()["sessions"][0]["session_info"]["itu"]

    yield {"access_token_cookie": access_token_cookie}


def test_register_temp_web(client, making_temp_web):
    access_token_cookie = making_temp_web["access_token_cookie"]
    base_registered_user_email = "test@example.com"
    base_registered_user_password = "mypassword123"
    official_registration_response = client.post(
        "/api/auth/register-web",
        json={
            "email": base_registered_user_email,
            "password": base_registered_user_password,
        },
        cookies={"access_token": access_token_cookie},
    )
    assert official_registration_response.status_code == 201

    # Make sure that the old token is invalidated
    old_token_response = client.get(
        "api/me/info", cookies={"access_token": access_token_cookie}
    )

    assert old_token_response.status_code == 401

    new_token_response = client.get(
        "api/me/info",
        cookies={
            "access_token": official_registration_response.cookies["access_token"]
        },
    )

    assert new_token_response.status_code == 200
