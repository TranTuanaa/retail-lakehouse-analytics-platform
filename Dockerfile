FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y openjdk-21-jdk git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "notebooks/test_spark_session.py"]