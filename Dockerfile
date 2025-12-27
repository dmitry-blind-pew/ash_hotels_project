FROM python:3.11.6

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD alembic upgrade head; python src/main.py

#CMD ["python", "src/main.py"]