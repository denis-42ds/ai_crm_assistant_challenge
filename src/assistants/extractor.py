import os
import requests
import json
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional

class LeadText(BaseModel):
    text: str

class ExtractedInfo(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None

def create_prompt(lead_text: str):
    return f"""
Ты — ассистент по заполнению карточек клиента. Твоя задача — извлечь из текста следующие данные: имя человека, название его компании и адрес электронной почты. Если какая-то информация отсутствует, оставь поле пустым. Верни ответ в формате JSON.

Текст запроса:
{lead_text}

Формат ответа:
{{"name": "...", "company": "...", "email": "..."}}
"""

def extract_info_with_llm(lead_text: str, api_key: str):
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

        raw_result = response.json()["choices"][0]["message"]["content"].strip()
        extracted_data = json.loads(raw_result)

        return extracted_data

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке запроса: {e}")
