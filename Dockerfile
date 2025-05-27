FROM python:3.11

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y curl wget gnupg && \
    apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libxcomposite1 libxdamage1 libxrandr2 libxss1 libasound2 libxshmfence1 libgbm1 libgtk-3-0 libx11-xcb1 && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Instala browsers para Playwright
RUN playwright install --with-deps

CMD ["python", "server.py"]
