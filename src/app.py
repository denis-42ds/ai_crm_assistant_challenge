import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Загружаем переменные окружения из .env-файла
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()

class LeadText(BaseModel):
    text: str

def create_prompt(lead_text: str):
    """
    Создаёт промпт для LLM на основе текста лида.
    """
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

@app.post("/classify")
async def classify_lead(lead: LeadText):
    """
    Принимает текст лида и возвращает его классификацию с помощью LLM.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured.")

    url = "https://amo-ai-challenge-1.up.railway.app/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "x-litellm-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    prompt = create_prompt(lead.text)

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Вызовет ошибку для плохих статусов HTTP

        result = response.json()
        classification = result["choices"][0]["message"]["content"].strip()

        # Проверяем, что ответ соответствует одному из наших тегов
        valid_tags = ["Горячий", "Тёплый", "Холодный"]
        if classification not in valid_tags:
            return {"classification": "Неизвестно"} # Обработка невалидного ответа

        return {"classification": classification}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе к LLM API: {e}")
