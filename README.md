# This is a simple chat completion service.

## 1. LLM model

Requirements:
- 1B-7B model (approx. 2GB-16GB memory)
- Run on 1 GPU (cloud GPU)
- Handles basic text completion/chat
- Low latency (sub-second responses for short prompts)
- Fits into budget cloud GPU (≤ $0.50/hr)

Models chosen via https://huggingface.co:
[LLaMA-2-7B](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
[gemma3:270m](https://huggingface.co/google/gemma-3-270m)

## 2. LLM serving engines

Requirements:
- Supports NVIDIA (optional CUDA)
- Easy to set up
- API integration, simple API access

Ollama | vLLM
https://github.com/alpine-docker/ollama

Steps:
1. [x] Run/test llms locally
2. [] Create/use a docker image
3. [] Choose cloud GPU offers
4. [] Setup cloud k8s
5. [] Deploy the service
6. [] Expose the service
7. [] Setup monitoring

## Usage

1. Env vars:

    export AWS_PROFILE=ak-dev
    export AWS_REGION=us-east-1
    export EKS_NAME=j-llm

2. aws eks update-kubeconfig --name ${EKS_NAME} --region ${AWS_REGION} --profile ${AWS_PROFILE} --alias ${EKS_NAME}
3. kubectl config use-context j-llm
4. kubectl apply -f deploy/

## Install

1. helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -f values.yaml -n j-llm

2. Pull gemma3:270m model

`
curl http://localhost:11434/api/pull -d '{
  "model": "gemma3:270m",

}'
`

3. Generate completion API

`
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
`
