import os
import requests
from fastapi import HTTPException
from pydantic import BaseModel

class LeadText(BaseModel):
    text: str

def create_prompt(lead_text: str):
    return f"""
Ты — ассистент по приоритизации лидов. Проанализируй текст запроса от клиента и присвой ему один из трёх тегов: Горячий, Тёплый или Холодный.

Определения:
Горячий: клиент имеет конкретный запрос, готов обсуждать сделку, бюджет и сроки.
Тёплый: клиент на этапе сбора информации, запрашивает кейсы, сравнивает предложения.
Холодный: клиент задает общие вопросы, не имеет конкретной потребности, просто изучает рынок.

Текст запроса:
{lead_text}

Ответ должен содержать только один тег, без дополнительных слов.
"""

def classify_lead_with_llm(lead_text: str, api_key: str):
    url = "https://amo-ai-challenge-1.up.railway.app/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "x-litellm-api-key": api_key,
        "Content-Type": "application/json"
    }

    prompt = create_prompt(lead_text)
    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        classification = response.json()["choices"][0]["message"]["content"].strip()

        valid_tags = ["Горячий", "Тёплый", "Холодный"]
        if classification not in valid_tags:
            return {"classification": "Неизвестно"}

        return {"classification": classification}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к LLM API: {e}")
