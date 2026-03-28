FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential gcc pkg-config && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir streamlit plotly pandas requests mysql-connector-python

COPY dashboard.py .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
