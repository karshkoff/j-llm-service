FROM alpine:latest

RUN apk add --no-cache curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin/:$PATH"
ENV PATH="/app/.venv/bin:$PATH"
ENV OLLAMA_MODEL="gemma3:270m"

WORKDIR /app

COPY ollama-exporter/ /app/

RUN uv sync --frozen

EXPOSE 8088

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
