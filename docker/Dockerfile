FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
