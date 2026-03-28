FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential gcc pkg-config && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY fraud_model.pkl .

EXPOSE 5000

CMD ["python", "app.py"]
