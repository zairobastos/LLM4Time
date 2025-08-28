FROM python:3.13.1-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential sqlite3 \
  && rm -rf /var/lib/apt/lists/* \
  && python -m pip install --upgrade pip \
  && pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD python database/create_database.py && python main.py
