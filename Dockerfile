FROM python:3.13.1-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential sqlite3 \
  && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
COPY requirements.txt requirements-streamlit.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-streamlit.txt

COPY . .

RUN pip install -e ./llm4time

EXPOSE 8501

ENTRYPOINT ["python", "app/main.py"]
