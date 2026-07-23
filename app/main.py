from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx

import asyncio
import random
from typing import Optional

from models import CadastralQuery
from schemas import QueryRequest, QueryResponse
from db import init_db, get_db
from lifespan import lifespan


app = FastAPI(title="Cadastral Service", lifespan=lifespan)

@app.get("/ping")
async def ping():
    return {"status": "ok"}



@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, db: AsyncSession = Depends(get_db)):
    db_query = CadastralQuery(
        cadastral_number=request.cadastral_number,
        latitude=request.latitude,
        longitude=request.longitude,
    )
    db.add(db_query)
    await db.commit()
    await db.refresh(db_query)

    try:
        async with httpx.AsyncClient(timeout=70.0) as client:
            response = await client.get("http://localhost:8000/result")
            response.raise_for_status()
            result = response.json()["result"]
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка обращения к внешнему серверу: {e}")

    db_query.result = result
    await db.commit()
    await db.refresh(db_query)

    return db_query

@app.get("/result")
async def results():
    delay = random.uniform(1, 60)
    await asyncio.sleep(delay)
    return {"result": random.choice([True, False])}


@app.get("/history", response_model=list[QueryResponse])
async def history(
    cadastral_number: Optional[str] = Query(None, description="Фильтр по кадастровому номеру"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CadastralQuery).order_by(CadastralQuery.created_at.desc())
    if cadastral_number:
        stmt = stmt.where(CadastralQuery.cadastral_number == cadastral_number)
    result = await db.execute(stmt)
    return result.scalars().all()

