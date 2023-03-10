FROM python:3.10

WORKDIR /app

COPY requirements.txt  ./
RUN pip install --upgrade --no-cache-dir -r requirements.txt

COPY src ./src
COPY alembic.ini ./
COPY migrations ./migrations

CMD ["uvicorn", "--factory", "src.api.main:api", "--host", "0.0.0.0", "--port", "8000"]
