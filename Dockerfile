FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN useradd -m dagster_user
USER dagster_user

WORKDIR /app/orchestration

RUN mkdir -p /tmp/dagster_home

ENV DAGSTER_HOME=/tmp/dagster_home

EXPOSE 3000

CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]
