import time
import random
import requests

URL = "https://ollama.leazardlabs.site/exporter/generate"

# List of example prompts
PROMPTS = [
    "What is your version?",
    "Explain Docker in simple terms.",
    "What is Python used for?",
    "Give me a random fun fact.",
    "Summarize the latest news.",
]

MODEL = "gemma3:270m"


def send_request(prompt):
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    try:
        response = requests.post(URL, json=payload)
        if response.status_code == 200:
            print(f"[OK] Prompt: {prompt} → Response: {response.json()}")
        else:
            print(f"[ERROR] Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] {e}")


def main():
    while True:
        prompt = random.choice(PROMPTS)
        send_request(prompt)
        time.sleep(20)


if __name__ == "__main__":
    main()
