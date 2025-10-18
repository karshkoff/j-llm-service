import os
import time
from fastapi import FastAPI, Request, Response
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from ollama import Client

# FastAPI
app = FastAPI(title="Ollama Generate Prometheus Exporter")

# Ollama client
ollama = Client(host=os.getenv("OLLAMA_URL", "http://localhost:11434"))

# Prometheus metrics
REQUEST_COUNT = Counter(
    "ollama_requests_total", "Total Ollama generate requests", ["model"]
)
REQUEST_ERRORS = Counter(
    "ollama_request_errors_total", "Failed Ollama generate requests", ["model"]
)
TTFT = Gauge("ollama_ttft_seconds", "Estimated Time to first token", ["model"])
TTLT = Gauge("ollama_ttlt_seconds", "Time to last token", ["model"])
GENERATION_TIME = Gauge(
    "ollama_generation_time_seconds", "Token generation time only", ["model"]
)
TPS = Gauge("ollama_tokens_per_second", "Token generation rate", ["model"])
LATENCY = Histogram(
    "ollama_request_latency_seconds", "End-to-end request latency", ["model"]
)


@app.post("/api/generate")
async def generate(request: Request):
    """
    Receive a text generation request, forward to Ollama /generate,
    compute metrics (TTFT, TTLT, TPS), and return the model output.

    Response metrics:
    total_duration: time spent generating the response
    load_duration: time spent in nanoseconds loading the model
    prompt_eval_count: number of tokens in the prompt
    prompt_eval_duration: time spent in nanoseconds evaluating the prompt
    eval_count: number of tokens in the response
    eval_duration: time in nanoseconds spent generating the response
    """
    data = await request.json()
    model = data.get("model", os.getenv("OLLAMA_MODEL", "gemma3:270m"))
    prompt = data.get("prompt", "")

    REQUEST_COUNT.labels(model).inc()
    start_time = time.time()

    try:
        # redirect request to Ollama /api/generate endpoint
        response = ollama.generate(model=model, prompt=prompt, stream=False)

        elapsed = time.time() - start_time
        LATENCY.labels(model).observe(elapsed)

        # Metrics calculations
        total_duration = response.get("total_duration", 0) / 1e9
        load_duration = response.get("load_duration", 0) / 1e9
        prompt_eval_duration = response.get("prompt_eval_duration", 0) / 1e9
        eval_count = response.get("eval_count", 0)
        eval_duration = response.get("eval_duration", 1) / 1e9

        # Time to first token (TTFT)
        ttft = (
            load_duration
            + prompt_eval_duration
            + (eval_duration / eval_count if eval_count > 0 else 0)
        )

        # Token generation only
        generation = total_duration - (load_duration + prompt_eval_duration)

        # Tokens per second
        tps = eval_count / eval_duration if eval_duration > 0 else 0

        # Update Prometheus metrics
        TTFT.labels(model).set(ttft)
        TTLT.labels(model).set(total_duration)
        GENERATION_TIME.labels(model).set(generation)
        TPS.labels(model).set(tps)

        res_dict = dict(response)
        res_dict.pop("context", None)

        res_dict.update(
            {
                "ttft_seconds": ttft,
                "ttlt_seconds": total_duration,
                "generation_time_seconds": generation,
                "tokens_per_second": tps,
            }
        )

        return res_dict

    except Exception as e:
        REQUEST_ERRORS.labels(model).inc()
        return {"error": str(e)}, 500


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
