# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501
EXPOSE 3003

HEALTHCHECK CMD curl --fail http://localhost:3003/_stcore/health

ENTRYPOINT ["streamlit", "run", "display.py", "--server.port=3003", "--server.address=0.0.0.0"]
