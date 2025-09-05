import os
import requests
from fastapi import HTTPException
from pydantic import BaseModel

class LeadText(BaseModel):
    text: str

def create_prompt(note_text: str):
    return f"""
Ты — ассистент-редактор. Твоя задача — взять текст заметки, исправить грамматические ошибки, улучшить её структуру и выделить ключевые моменты. Отформатируй результат, чтобы он был легко читаем.

Оригинальный текст заметки:
{note_text}

Отформатированный результат:
"""

def edit_note_with_llm(note_text: str, api_key: str):
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

        edited_text = response.json()["choices"][0]["message"]["content"].strip()

        return {"edited_note": edited_text}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке запроса: {e}")
