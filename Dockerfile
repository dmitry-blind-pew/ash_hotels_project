FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements-prod.txt requirements-prod.txt
RUN pip install --upgrade pip && pip install -r requirements-prod.txt

COPY . .

CMD alembic upgrade head; python src/main.py

#CMD ["python", "src/main.py"]