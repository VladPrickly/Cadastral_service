from fastapi import FastAPI
from contextlib import asynccontextmanager

from db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
