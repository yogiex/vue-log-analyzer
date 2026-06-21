D# Gunakan Python slim (ukuran kecil, cukup untuk production)
FROM python:3.11-slim

WORKDIR /app

# Install dependensi sistem yang diperlukan (untuk mysqlclient, dll.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        gcc \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Salin requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode aplikasi
COPY app.py .
COPY config.py .
COPY services/ ./services/
COPY templates/ ./templates/
COPY static/ ./static/

# Port yang digunakan Flask
EXPOSE 8443

# Jalankan dengan gunicorn (lebih stabil) atau python app.py
CMD ["gunicorn", "--bind", "0.0.0.0:8443", "app:app"]