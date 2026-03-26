def test_routes(client):
    """This test prints out all available API routes."""
    print("Printing API routes...")
    for route in client.app.routes:
        print(route.path)

def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "mypassword123"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_register_duplicate_email(client):
    # Register once
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "mypassword123"
    })
    # Try again with same email
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "differentpassword"
    })
    assert response.status_code == 400

def test_login_success(client):
    # Register first
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "mypassword123"
    })
    # Then login
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "mypassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "mypassword123"
    })
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_missing_email(client):
    response = client.post("/api/auth/login", json={
        "password": "mypassword123"
    })
    assert response.status_code == 422  # Pydantic catches this