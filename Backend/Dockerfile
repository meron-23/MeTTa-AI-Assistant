# Prevent Python from writing .pyc files and force stdout/stderr to be unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM python:3.11-slim

WORKDIR /app

# Upgrade pip first, then install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Allow flexible reload flag via env variable
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 ${RELOAD}"]
