# Tron Wallet Info Service

Микросервис для получения информации о кошельках в сети Tron (TRX): баланс, bandwidth и energy. Все обращения к сервису сохраняются в базу данных. Реализованы REST API эндпоинты и базовые тесты.

## 🚀 Быстрый старт

1. **Клонировать репозиторий:**

```bash
git clone https://github.com/BOPOH1243/ttTron.git
cd ttTron
```

2. **Запуск всего проекта (приложение + PostgreSQL + Nginx) через Docker Compose:**

```bash
sudo docker-compose up -d
```

3. **Открыть документацию API (Swagger UI):**

Перейдите в браузере по адресу:

```
http://localhost/docs
```

---

## 📦 Стек технологий

- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- TronPy
- Pytest
- Docker + Docker Compose
- Nginx (реверс-прокси)

---

## 🧪 Тестирование

Проект содержит юнит- и интеграционные тесты. Для запуска:

```bash
pytest
```

---

## 📁 Структура проекта

- `app/` — код микросервиса
- `models/` — SQLAlchemy-модели
- `schemas/` — Pydantic-схемы
- `core/` — конфигурация и подключение к БД
- `tests/` — тесты
- `docker-compose.yml` — сборка всего проекта (FastAPI + БД + Nginx)

---

## 📬 Контакты

Для вопросов и предложений: [issues](https://github.com/BOPOH1243/ttTron/issues)