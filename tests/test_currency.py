from datetime import date

from httpx import AsyncClient


async def test_list_currencies_unauthorized(client: AsyncClient):
    resp = await client.get("/currencies")
    assert resp.status_code == 401


async def test_get_currency_unauthorized(client: AsyncClient):
    resp = await client.get("/currencies/RUB")
    assert resp.status_code == 401


async def test_get_latest_rate_not_found(
    client: AsyncClient,
    auth_headers: dict,
):
    resp = await client.get("/currencies/hello", headers=auth_headers)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Currency not found"


async def test_get_history_not_found(
    client: AsyncClient,
    auth_headers: dict,
):
    resp = await client.get(
        "/currencies/XYZ/history",
        params={"start_date": "2026-01-01", "end_date": "2026-01-31"},
        headers=auth_headers,
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Currency not found"


async def test_get_all_rates_not_found(
    client: AsyncClient, auth_headers: dict
):
    resp = await client.get("/currencies/hello/all", headers=auth_headers)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Currency not found"


async def test_list_currencies_with_data(
    client: AsyncClient,
    auth_headers: dict,
    add_currency_to_db: dict,
):
    resp = await client.get("/currencies", headers=auth_headers)
    assert resp.status_code == 200
    codes = {c["char_code"] for c in resp.json()}
    assert "RUB" in codes
    assert "TNG" in codes


async def test_get_latest_rate(
    client: AsyncClient,
    auth_headers: dict,
    add_currency_to_db: dict,
):
    resp = await client.get("/currencies/RUB", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "rate" in data
    assert "date" in data
    assert data["date"] == date.today().isoformat()


async def test_get_history_in_range(
    client: AsyncClient,
    auth_headers: dict,
    add_currency_to_db: dict,
):
    today = date.today().isoformat()
    resp = await client.get(
        "/currencies/RUB/history",
        params={"start_date": today, "end_date": today},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1


async def test_get_history_missing_params(
    client: AsyncClient,
    auth_headers: dict,
):
    resp = await client.get("/currencies/RUB/history", headers=auth_headers)
    assert resp.status_code == 422


async def test_get_all_rates(
    client: AsyncClient,
    auth_headers: dict,
    add_currency_to_db: dict,
):
    resp = await client.get("/currencies/RUB/all", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
