FROM python:3.11-slim

# Instala dependencias necesarias para Playwright
RUN apt-get update && apt-get install -y \
    curl wget gnupg \
    libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 \
    && apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install --with-deps

CMD ["python", "server.py"]
