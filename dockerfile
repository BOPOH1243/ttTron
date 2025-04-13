# Используем официальный Python образ не ниже версии 3.10
FROM python:3.10-slim

# Назначаем переменную окружения для поиска модулей
ENV PYTHONPATH=/app

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта (в частности, каталог app)
COPY . .

# Запускаем приложение (предполагается, что внутри main.py вызывается uvicorn)
CMD ["python", "app/main.py"]
