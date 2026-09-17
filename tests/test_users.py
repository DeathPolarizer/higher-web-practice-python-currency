from httpx import AsyncClient


async def test_register_success(client: AsyncClient):
    resp = await client.post(
        "/users/register",
        json={
            "email": "new@example.com",
            "username": "new",
            "password": "new",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert data["username"] == "new"


async def test_register_duplicate_email(
    client: AsyncClient,
    registered_user: dict,
):
    resp = await client.post(
        "/users/register",
        json={
            "email": registered_user["email"],
            "username": "other",
            "password": "pass123",
        },
    )
    assert resp.status_code == 409
    assert resp.json()["detail"] == "User already exists"


async def test_get_user_by_id(
    client: AsyncClient,
    registered_user: dict,
    auth_headers: dict,
):
    resp = await client.get(
        f"/users/{registered_user['id']}",
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == registered_user["id"]
    assert data["email"] == registered_user["email"]


async def test_get_user_by_id_not_found(
    client: AsyncClient,
    auth_headers: dict,
):
    resp = await client.get("/users/400", headers=auth_headers)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "User not found"


async def test_get_user_by_id_unauthorized(
    client: AsyncClient,
    registered_user: dict,
):
    resp = await client.get(f"/users/{registered_user['id']}")
    assert resp.status_code == 401


async def test_get_user_by_email(
    client: AsyncClient,
    registered_user: dict,
    auth_headers: dict,
):
    resp = await client.get(
        f"/users/email/{registered_user['email']}", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["email"] == registered_user["email"]


async def test_get_user_by_email_not_found(
    client: AsyncClient,
    auth_headers: dict,
):
    resp = await client.get(
        "/users/email/nobody@example.com", headers=auth_headers
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "User not found"


async def test_get_user_by_email_unauthorized(
    client: AsyncClient,
    registered_user: dict,
):
    resp = await client.get(f"/users/email/{registered_user['email']}")
    assert resp.status_code == 401


async def test_update_username(
    client: AsyncClient,
    registered_user: dict,
    auth_headers: dict,
):
    resp = await client.put(
        "/users",
        json={"username": "updated_name"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["username"] == "updated_name"


async def test_update_password(
    client: AsyncClient,
    registered_user: dict,
    auth_headers: dict,
):
    resp = await client.put(
        "/users",
        json={"password": "newpassword456"},
        headers=auth_headers,
    )
    assert resp.status_code == 200

    login_resp = await client.post(
        "/auth/login",
        json={"email": registered_user["email"], "password": "newpassword456"},
    )
    assert login_resp.status_code == 200


async def test_update_user_unauthorized(client: AsyncClient):
    resp = await client.put("/users", json={"username": "hacker"})
    assert resp.status_code == 401
