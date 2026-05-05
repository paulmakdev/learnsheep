def test_me_info_success(client):
    original_email = "test@example.com"
    response = client.post(
        "/api/auth/register",
        json={"email": original_email, "password": "mypassword123"},
    )
    access_token = response.json()["access_token"]

    response = client.get(
        "/api/me/info",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert "email" in response.json()
    assert "display_name" in response.json()

    assert response.json()["email"] == original_email
