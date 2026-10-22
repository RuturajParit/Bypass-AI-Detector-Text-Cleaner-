
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends tar \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

CMD ["python", "-u", "src/cleaner.py"]
