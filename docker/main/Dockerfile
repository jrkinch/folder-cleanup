FROM python:3.11-slim-buster

WORKDIR /app

#Copy pyproject.toml and source code
COPY pyproject.toml .
COPY src/ ./src/

RUN pip install --no-cache-dir .

CMD ["python", "src/main.py"]
