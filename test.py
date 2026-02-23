#en başta ollama çalışıyor mu diye test edip baktım 

import requests

def ask_mistral(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

print(ask_mistral("Classify this email: I want a refund"))
