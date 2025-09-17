from fastapi.testclient import TestClient
from src.app import app
import os

client = TestClient(app)

def test_classify_endpoint_with_api_key(mocker):
    """
    Тестирует эндпоинт /classify, мокируя вызов к LLM.
    """
    # Мокируем функцию, которая делает внешний API-вызов, чтобы избежать реальных запросов
    mocker.patch('src.assistants.classifier.classify_lead_with_llm', return_value={"category": "Hot"})
    mocker.patch.dict(os.environ, {'API_KEY': 'test_key'})

    response = client.post("/classify", json={"text": "Hello, I am interested in your product."})
    assert response.status_code == 200
    assert response.json() == {"category": "Hot"}

def test_extract_info_endpoint_with_api_key(mocker):
    """
    Тестирует эндпоинт /extract-info, мокируя вызов к LLM.
    """
    mocker.patch('src.assistants.extractor.extract_info_with_llm', return_value={"contact_name": "Ivan", "company_name": "Roga i Kopyta"})
    mocker.patch.dict(os.environ, {'API_KEY': 'test_key'})

    response = client.post("/extract-info", json={"text": "Меня зовут Иван из компании Рога и Копыта."})
    assert response.status_code == 200
    assert response.json()["contact_name"] == "Ivan"

def test_risk_assessment_endpoint_with_api_key(mocker):
    """
    Тестирует эндпоинт /risk-assessment, мокируя вызов к LLM.
    """
    mocker.patch('src.assistants.risk_assessor.assess_risk_with_llm', return_value={"is_at_risk": True, "reason": "Клиент не отвечает"})
    mocker.patch.dict(os.environ, {'API_KEY': 'test_key'})

    response = client.post("/risk-assessment", json={"text": "Клиент не отвечает уже неделю"})
    assert response.status_code == 200
    assert response.json()["is_at_risk"] == True

def test_endpoint_without_api_key():
    """
    Тестирует, что эндпоинт возвращает ошибку, если API-ключ не настроен.
    """
    mocker.patch.dict(os.environ, clear=True)

    response = client.post("/classify", json={"text": "Test"})
    assert response.status_code == 500
    assert "API key is not configured" in response.json()["detail"]
