# app/llm.py
import requests
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

def generate_questions_from_fields(fields: List[str], language: str) -> List[Dict]:
    system_prompt = (
        "You are a helpful assistant that creates user-friendly questions "
        "to collect information for filling out a form. "
        "You must respond ONLY in valid JSON. "
        "Output format: [{\"id\": \"q1\", \"field_name\": \"Full Name\", \"question_text\": \"...\"}, ...]."
    )

    user_prompt = (
        f"Fields: {fields}\n"
        f"Language: {language}\n\n"
        "For each field, create ONE clear question in the given language that a normal person can answer. "
        "Keep questions short and polite."
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
    resp.raise_for_status()
    content = resp.json()["message"]["content"]

    # content should be JSON text; parse it
    import json
    try:
        questions = json.loads(content)
    except json.JSONDecodeError:
        # fallback: wrap in list or do minimal cleanup
        questions = []
    return questions
