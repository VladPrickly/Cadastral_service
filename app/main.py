from fastapi import FastAPI
from contextlib import asynccontextmanager

from db import init_db, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Cadastral Service", lifespan=lifespan)

@app.get("/ping")
async def ping():
    return {"status": "ok"}

