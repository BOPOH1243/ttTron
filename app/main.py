#app/main.py
from sqlalchemy import func, select
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, engine, Base
from app.models.query_records import QueryRecord
from app.schemas.query_records import QueryRecordCreate, QueryRecordResponse, QueryRecordsListResponse
from tronpy import Tron
import asyncio
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def get_tron_info(address: str) -> dict:
    """
    Получаем информацию о кошельке в сети Tron:
        - баланс TRX
        - bandwidth (используем значение freeNetLimit, если доступно)
        - energy (используем значение energy_limit, если доступно)
    """
    try:
        client = Tron()
        balance = client.get_account_balance(address)
        resources = client.get_account_resource(address)
        bandwidth = resources.get("freeNetLimit", "Неизвестно")
        energy = resources.get("energy_limit", "Неизвестно")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка получения данных из сети Tron: {str(e)}")
    return {"balance": balance, "bandwidth": bandwidth, "energy": energy}

@app.post("/query", response_model=dict)
async def query_address(query_data: QueryRecordCreate, db: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для запроса информации по адресу.
    Получает данные через tronpy и сохраняет запись в БД.
    """
    info = get_tron_info(query_data.address)
    
    record = QueryRecord(address=query_data.address)
    db.add(record)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении записи в БД: {str(e)}")
    return {**info, "message": "Данные успешно получены и сохранены"}

@app.get("/records", response_model=QueryRecordsListResponse)
async def get_records(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    """
    Эндпоинт для получения списка последних записей с пагинацией.
    """
    offset = (page - 1) * size

    # Используем select и func.count() для подсчёта общего количества записей
    total_query = await db.execute(select(func.count()).select_from(QueryRecord))
    total = total_query.scalar() or 0

    # Получаем записи с использованием ORM запроса и сортировки по дате в обратном порядке
    result = await db.execute(
        select(QueryRecord).order_by(QueryRecord.queried_at.desc()).offset(offset).limit(size)
    )
    records = result.scalars().all()

    records_list = [QueryRecordResponse.from_orm(record) for record in records]
    
    return QueryRecordsListResponse(records=records_list, total=total, page=page, size=size)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)