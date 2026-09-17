from httpx import AsyncClient


async def test_login_success(
    client: AsyncClient,
    registered_user: dict,
):
    resp = await client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(
    client: AsyncClient,
    registered_user: dict,
):
    resp = await client.post(
        "/auth/login",
        json={"email": registered_user["email"], "password": "wrongpassword"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


async def test_login_unknown_email(client: AsyncClient):
    resp = await client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "password"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


async def test_refresh_success(
    client: AsyncClient,
    registered_user: dict,
):
    login_resp = await client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    refresh_token = login_resp.json()["refresh_token"]

    resp = await client.post(
        "/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


async def test_refresh_with_invalid_token(client: AsyncClient):
    resp = await client.post(
        "/auth/refresh", json={"refresh_token": "invalid.jwt.token"}
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


async def test_refresh_with_access_token_rejected(
    client: AsyncClient,
    registered_user: dict,
):
    """Access token must not be accepted at the refresh endpoint."""
    login_resp = await client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    access_token = login_resp.json()["access_token"]

    resp = await client.post(
        "/auth/refresh", json={"refresh_token": access_token}
    )
    assert resp.status_code == 401
