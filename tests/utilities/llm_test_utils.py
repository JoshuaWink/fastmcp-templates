import os
import requests

LLM_URL = os.environ.get("LLM_URL", "http://localhost:8080/v1/chat/completions")
LLM_MODEL = "gpt-4.1"

def llm_call(messages, model=LLM_MODEL, url=LLM_URL, timeout=30):
    payload = {
        "model": model,
        "messages": messages
    }
    resp = requests.post(url, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    # Accept both OpenAI and raw JSON response formats
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    return data
