FROM python:3.12-slim

WORKDIR /app

# Скопировать requirements
COPY requirements.txt .

# Установить зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем код проекта
COPY . /app

# Запуск FastAPI сразу
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
