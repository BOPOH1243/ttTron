import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import Base, get_db

# Создаём движок для in-memory SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
)

# Создаём новую фабрику сессий для тестов
async_session_maker = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

# Переопределяем зависимость get_db для тестового движка
async def override_get_db():
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Фикстура для создания таблиц перед тестированием
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # Создание таблиц в базе данных
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Удаление таблиц после тестов (при желании)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(autouse=True)
async def delay_between_tests():
    await asyncio.sleep(1)
    yield

@pytest.mark.asyncio
async def test_query_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"address": "TWBPGLwQw2EbqYLLw1DJnTDt2ZQ9yJW1JJ"}
        response = await client.post("/query", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "balance" in data
        assert "message" in data


@pytest.mark.asyncio
async def test_get_records():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"address": "TWBPGLwQw2EbqYLLw1DJnTDt2ZQ9yJW1JJ"}
        create_response = await client.post("/query", json=payload)
        print(create_response.json())
        assert create_response.status_code == 200
        response = await client.get("/records?page=1&size=10")
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert "records" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert data["total"] >= 1
        assert len(data["records"]) > 0