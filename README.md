# This is a simple chat completion service.

## 1. LLM model

Requirements:
- 1B-7B model
- Run on 1 GPU (cloud GPU)
- Handles basic text completion/chat
- Low latency (sub-second responses for short prompts)
- Fits into budget cloud GPU (≤ $0.50/hr)

Model can be randomly chosen:
LLaMA-2-7B | Mistral-7B-Instruct-v0.2

## 2. LLM serving engines

Requirements:
- Supports NVIDIA (optional CUDA)
- Easy to set up
- API integration, simple API access

Ollama | vLLM

