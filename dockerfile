FROM python:3.13-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry \
 && poetry install --no-root

COPY src ./src
COPY .env .env

CMD ["poetry", "run", "uvicorn", "src.main:create_app", "--host", "0.0.0.0", "--port", "8001", "--factory", "--reload"]