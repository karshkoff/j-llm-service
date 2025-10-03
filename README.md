# This is a simple chat completion service.

## 1. LLM model

Requirements:
- 1B-7B model
- Run on 1 GPU (cloud GPU)
- Handles basic text completion/chat
- Low latency (sub-second responses for short prompts)
- Fits into budget cloud GPU (≤ $0.50/hr)

Models chosen via https://huggingface.co:
[LLaMA-2-7B](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
[Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)

## 2. LLM serving engines

Requirements:
- Supports NVIDIA (optional CUDA)
- Easy to set up
- API integration, simple API access

Ollama | vLLM

Steps:
1. [x] Run/test llms locally
2. [] Create/use a docker image
3. [] Choose cloud GPU offers
4. [] Setup cloud k8s
5. [] Deploy the service
6. [] Expose the service
7. [] Setup monitoring
