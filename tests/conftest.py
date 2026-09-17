import os
from datetime import date
from decimal import Decimal

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import core.db
import main as main_module
from core.db import Base, get_db
from domain.currency.models import Currency, ExchangeRate
from main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

os.environ.setdefault("APP_VERSION", "test")
os.environ.setdefault("APP_NAME", "Currency Service Test")
os.environ.setdefault("SECRET_KEY", "test")
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("DATABASE_URL_SYNC", "sqlite:///:memory:")


@pytest_asyncio.fixture
async def client(monkeypatch):
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    monkeypatch.setattr(core.db, "engine", test_engine)
    monkeypatch.setattr(core.db, "AsyncSessionLocal", TestSessionLocal)
    monkeypatch.setattr(main_module, "engine", test_engine)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def registered_user(client: AsyncClient) -> dict:
    payload = {
        "email": "user@example.com",
        "username": "string",
        "password": "string",
    }
    resp = await client.post("/users/register", json=payload)
    assert resp.status_code == 201
    return {**resp.json(), "password": payload["password"]}


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, registered_user: dict) -> dict:
    resp = await client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def add_currency_to_db(client: AsyncClient) -> dict:
    async with core.db.AsyncSessionLocal() as session:
        usd = Currency(
            char_code="RUB",
            num_code="1",
            name="Рубли РФ",
            nominal=1,
        )
        eur = Currency(
            char_code="TNG",
            num_code="22",
            name="Тенге",
            nominal=100,
        )
        session.add_all([usd, eur])
        await session.flush()

        today = date.today()
        session.add_all(
            [
                ExchangeRate(
                    currency_id=usd.id,
                    rate=Decimal("10.790000"),
                    date=today,
                ),
                ExchangeRate(
                    currency_id=eur.id,
                    rate=Decimal("100.850000"),
                    date=today,
                ),
            ]
        )
        await session.commit()

    return {
        "RUB": Decimal("10.790000"),
        "TNG": Decimal("100.850000"),
        "date": today,
    }
