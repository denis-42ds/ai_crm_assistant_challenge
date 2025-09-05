import os
import requests
import json
from fastapi import HTTPException
from pydantic import BaseModel

class NoteText(BaseModel):
    text: str

def create_prompt(note_text: str):
    return f"""
Ты — AI-ассистент для оценки рисков сделок. Проанализируй текст из заметки или переписки и определи, есть ли признаки того, что сделка "зависла" или находится под угрозой. Признаками риска могут быть: отсутствие ответа от клиента, перенос встречи, долгая пауза в коммуникации, выражение неуверенности.

Ответь строго в формате JSON, где "is_at_risk" - это булево значение (true/false), а "reason" - краткое объяснение, почему сделка рискованна, или "нет".

Текст для анализа:
{note_text}

Пример формата ответа:
{{"is_at_risk": true, "reason": "Клиент не отвечает на звонки уже неделю"}}
{{"is_at_risk": false, "reason": "нет"}}
"""

def assess_risk_with_llm(note_text: str, api_key: str):
    url = "https://amo-ai-challenge-1.up.railway.app/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "x-litellm-api-key": api_key,
        "Content-Type": "application/json"
    }

    prompt = create_prompt(note_text)
    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        raw_result = response.json()["choices"][0]["message"]["content"].strip()
        risk_data = json.loads(raw_result)

        return risk_data

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке запроса: {e}")
