FROM python:3.11-slim-buster

WORKDIR /app

#Copy pyproject.toml and source code
COPY pyproject.toml .
COPY src/ ./src/
COPY tests/ ./tests/

RUN pip install --no-cache-dir .

CMD ["python", "-m", "pytest", "-v"]
