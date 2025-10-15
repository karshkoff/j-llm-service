#!/usr/bin/env python3
import time
import json
import requests
from flask import Flask, Response
from prometheus_client import Gauge, Counter, generate_latest, CONTENT_TYPE_LATEST

OLLAMA_URL = "http://host.docker.internal:11434"
MODEL = "gemma3:270m"

app = Flask(__name__)

# Prometheus metrics
ttft_gauge = Gauge('ollama_ttft_seconds', 'Time to first token in seconds', ['model'])
ttlt_gauge = Gauge('ollama_ttlt_seconds', 'Time to last token in seconds', ['model'])
request_counter = Counter('ollama_request_total', 'Number of requests made', ['model', 'status'])

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/probe")
def probe():
    """Trigger a test Ollama prompt and record timing metrics"""
    prompt = "What is the capital of France?"
    model = MODEL

    url = f"{OLLAMA_URL}/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": model, "prompt": prompt, "stream": True}

    start_time = time.time()
    first_token_time = None
    last_token_time = None

    try:
        with requests.post(url, headers=headers, data=json.dumps(data), stream=True, timeout=60) as r:
            for line in r.iter_lines():
                if not line:
                    continue
                if first_token_time is None:
                    first_token_time = time.time()
                last_token_time = time.time()

        if first_token_time and last_token_time:
            ttft = first_token_time - start_time
            ttlt = last_token_time - start_time
            ttft_gauge.labels(model=model).set(ttft)
            ttlt_gauge.labels(model=model).set(ttlt)
            request_counter.labels(model=model, status="success").inc()
        else:
            request_counter.labels(model=model, status="no_tokens").inc()

    except Exception as e:
        print("Error probing Ollama:", e)
        request_counter.labels(model=model, status="error").inc()

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9105)
