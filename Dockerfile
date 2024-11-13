# Використовуємо офіційний Python образ
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли проекту в контейнер
COPY . /app/

# Встановлюємо залежності з requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт, якщо потрібно (наприклад для сервера)
EXPOSE 8000

# Запускаємо main.py
CMD ["python", "main.py"]


