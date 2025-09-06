import os
import json
import requests
from pydantic import BaseModel
from fastapi import HTTPException

class NoteText(BaseModel):
    text: str

class RiskAssessment(BaseModel):
    is_at_risk: bool
    reason: str

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
    if not api_key:
        raise HTTPException(status_code=500, detail="API key is not configured.")

    llm_url = os.getenv("LLM_API_URL", "https://amo-ai-challenge-1.up.railway.app/v1/chat/completions")
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
        response = requests.post(llm_url, headers=headers, json=payload)
        response.raise_for_status()

        raw_result = response.json()["choices"][0]["message"]["content"].strip()

        try:
            risk_data = json.loads(raw_result)
            # Проверяем, что ответ соответствует ожидаемому формату
            if isinstance(risk_data, dict) and "is_at_risk" in risk_data and "reason" in risk_data:
                return risk_data
            else:
                raise ValueError("Ответ LLM имеет некорректный формат.")
        
        except json.JSONDecodeError:
            raise ValueError("Ответ LLM не является валидным JSON.")
        
    except (requests.exceptions.RequestException, ValueError) as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке запроса: {e}")
