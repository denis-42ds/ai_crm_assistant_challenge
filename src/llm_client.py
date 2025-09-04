import requests
import json

def create_prompt(lead_text):
    """
    Создает промпт для LLM на основе текста лида.
    """
    prompt = f"""
Ты — ассистент по приоритизации лидов. Проанализируй текст запроса от клиента и присвой ему один из трёх тегов: Горячий, Тёплый или Холодный.

Определения:
Горячий: клиент имеет конкретный запрос, готов обсуждать сделку, бюджет и сроки.
Тёплый: клиент на этапе сбора информации, запрашивает кейсы, сравнивает предложения.
Холодный: клиент задает общие вопросы, не имеет конкретной потребности, просто изучает рынок.

Текст запроса:
{lead_text}

Ответ должен содержать только один тег, без дополнительных слов.
"""
    return prompt

def classify_lead_with_llm(lead_text, api_key):
    """
    Отправляет запрос к API LLM для классификации лида.
    """
    url = "https://amo-ai-challenge-1.up.railway.app/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "x-litellm-api-key": api_key,
        "Content-Type": "application/json"
    }

    prompt = create_prompt(lead_text)

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Вызывает ошибку для плохих статусов HTTP

        result = response.json()
        # Извлекаем текст ответа из JSON
        classification = result["choices"][0]["message"]["content"].strip()
        return classification
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к LLM API: {e}")
        return "Ошибка"
