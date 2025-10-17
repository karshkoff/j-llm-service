# Use a Python base image
FROM python:3.11-slim

# Install dependencies for uv
RUN apt-get update && apt-get install -y curl build-essential

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY uv.lock .
COPY ollama_exporter.py .

# Install project dependencies using uv
RUN uv sync --locked --no-dev --no-install-project

# Expose the application port
EXPOSE 11808

# Set environment variables for the application
ENV OLLAMA_URL=http://localhost:11434
ENV OLLAMA_MODEL=gemma3:270m

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "ollama_exporter:app", "--host", "0.0.0.0", "--port", "11808"]
