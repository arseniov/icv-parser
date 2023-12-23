# syntax=docker/dockerfile:1.2
FROM --platform=${BUILDPLATFORM} python:3.9-slim AS builder

WORKDIR /app

COPY ./ /app/

RUN mkdir /app/data

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        software-properties-common \
        git \
    && pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install --no-cache-dir streamlit \
    && apt-get purge -y --auto-remove build-essential git \
    && rm -rf /var/lib/apt/lists/* /root/.cache

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

ARG ICV_USERNAME
ARG ICV_PASSWORD
ENV ICV_USERNAME=${ICV_USERNAME}
ENV ICV_PASSWORD=${ICV_PASSWORD}

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
