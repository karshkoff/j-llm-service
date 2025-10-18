FROM alpine:latest

RUN apk add --no-cache curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin/:$PATH"
ENV PATH="/app/.venv/bin:$PATH"
ENV OLLAMA_URL="http://host.docker.internal:11434"
ENV OLLAMA_MODEL="gemma3:270m"

WORKDIR /app

COPY pyproject.toml uv.lock /app/
COPY ollama_exporter.py /app

RUN uv sync --frozen

EXPOSE 8088

# FastAPI app with uvicorn
CMD ["uvicorn", "ollama_exporter:app", "--host", "0.0.0.0", "--port", "8088"]
