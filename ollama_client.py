#llm motorum burası, en önemli yer 

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
#"mistral-7b-v0.1.Q4_0.gguf"
#"mistral"

def ask_llm(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False #tüm text bir kerede geliyor demek, Ram'e yük biniyo
        }
    )

    return response.json()["response"].strip()
