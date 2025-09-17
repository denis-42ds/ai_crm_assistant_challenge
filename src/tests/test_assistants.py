from src.assistants.risk_assessor import create_prompt

def test_create_prompt_content():
    """Тестирует, что функция create_prompt создает ожидаемый текст запроса."""
    note_text = "Клиент не отвечает на звонки."
    expected_substring = "Клиент не отвечает на звонки."
    prompt = create_prompt(note_text)
    assert expected_substring in prompt
    assert "Признаки риска могут быть" in prompt
    assert "Ответь строго в формате JSON" in prompt
