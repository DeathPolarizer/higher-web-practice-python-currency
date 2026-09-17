from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import domain.currency.models  # noqa
import domain.users.models  # noqa
from api.auth.router import router as auth_router
from api.currency.router import router as currency_router
from api.users.router import router as users_router
from core.config import settings
from core.db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    version=settings.APP_VERSION,
    title=settings.APP_NAME,
    description="Python service for parsing and check currency rate",
    lifespan=lifespan,
)


app.include_router(currency_router)
app.include_router(users_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        timeout_graceful_shutdown=10,
        use_colors=True,
    )
