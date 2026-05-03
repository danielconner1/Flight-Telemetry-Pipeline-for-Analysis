FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -e .

CMD ["dagster", "api", "grpc", "-m", "orchestration.orchestration.defs"]