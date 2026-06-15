import uvicorn
from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.currency.router import router as currency_router
from api.users.router import router as users_router

app = FastAPI()
app.include_router(currency_router)
app.include_router(users_router)
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', reload=True)
