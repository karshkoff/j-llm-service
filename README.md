# PoC of a simple chat/completion service powered by an LLM

## Requirements

### LLM Model

- 1B-7B model (approx. 2GB-16GB memory)
- Run on 1 GPU (cloud GPU)
- Handles basic text completion/chat
- Low latency (sub-second responses for short prompts)
- Fits into budget cloud GPU (≤ $0.50/hr)

Search models on https://huggingface.co:

- [LLaMA-2-7B](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
- [gemma3:270m](https://huggingface.co/google/gemma-3-270m) (in use)

### Model serving engines

- Supports NVIDIA ([CUDA](https://developer.nvidia.com/cuda-toolkit))
- Easy to set up
- API integration, simple API access

Engines:

- slim [Ollama](https://github.com/alpine-docker/ollama) (in use)
- [vLLM](https://docs.vllm.ai/en/latest/)

## Deploy EKS infra

Use [j-llm-infra](https://github.com/karshkoff/j-llm-infra/blob/main/README.md)

## Deploy ollama

The application should be deployed by github actions,
if any issue use follow steps to deploy:

1. Env vars:

```
export AWS_PROFILE=ak-dev
export AWS_REGION=us-east-1
export EKS_NAME=j-llm
export ALLOW_CIDR=$(curl ifconfig.me)/32
```

AWS_PROFILE - [credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html) for current AWS account
ALLOW_CIDR - limit inbound traffic for AWS ALB

2. Update kubeconfig

```
aws eks update-kubeconfig --name ${EKS_NAME} --region ${AWS_REGION} --profile ${AWS_PROFILE} --alias ${EKS_NAME}
```

3. Chose cluster context

```
kubectl config use-context j-llm
```

4. Create ollama namespace

```
kubectl create namespace ollama
```

5. Deploy Ollama

```
kubectl apply -f k8s/app
```

6. Deploy ALB listeners


```
envsubst < k8s/ingress/ollama.yaml | kubectl apply -f -
```

```
envsubst < k8s/ingress/grafana.yaml | kubectl apply -f -
```

### Demo

1. Verify Ollama endpoints

```
https://ollama.leazardlabs.site/
```

2. Pull gemma3:270m model

```
curl https://ollama.leazardlabs.site/api/pull -d '{
  "model": "gemma3:270m"
}'
```

3. Test model, connect to local Open-webui

```
docker run -d --rm \
  -p 3030:8080 \
  -e OLLAMA_BASE_URL=https://ollama.leazardlabs.site \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

4. Test ollama API

```
curl https://ollama.leazardlabs.site/api/generate -d '{
  "model": "gemma3:270m",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

5. Test monitoring (using proxy - ollama-exporter)

Run test workload by:

```
python tests/ollama-exporter-workload.py
```

or a single call

```
curl https://ollama.leazardlabs.site/exporter/generate -d '{
  "model": "gemma3:270m",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

6. Verify ollama-exporter metrics

```
curl https://ollama.leazardlabs.site/metrics
```


7. Monitoring dashboard

Add grafana dashboard:

```
export GRAFANA_PSWD=$(kubectl get secret -n monitoring prometheus-stack-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode; echo -n)
```

```
curl -u admin:$GRAFANA_PSWD \
  -H "Content-Type: application/json" \
  -X POST https://grafana.leazardlabs.site/api/dashboards/db \
  -d @monitoring/ollama-dashboard.json
```

```
https://grafana.leazardlabs.site
```
