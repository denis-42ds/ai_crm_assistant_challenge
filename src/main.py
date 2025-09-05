import os
from dotenv import load_dotenv
from data_manager import load_leads, save_results
from llm_client import classify_lead_with_llm

def main():
    # Загружаем переменные окружения из .env-файла
    load_dotenv()
    # Получаем API-ключ
    API_KEY = os.getenv("API_KEY")

    if not API_KEY:
        print("Ошибка: API-ключ не найден. Убедитесь, что он прописан в файле .env")
        return

    # Пути к файлам
    data_dir = os.path.join(os.getcwd(), '..', 'data')
    leads_file = os.path.join(data_dir, 'leads.json')
    results_file = os.path.join(data_dir, 'processed_leads.csv')

    # Загружаем тестовые данные
    leads = load_leads(leads_file)
    if not leads:
        print("Нет данных для обработки. Завершение работы.")
        return

    classified_leads = []
    print("Начинаем классификацию лидов...")

    for lead in leads:
        lead_id = lead['id']
        lead_text = lead['text']

        print(f"\nОбработка лида #{lead_id}...")

        # Классифицируем лид с помощью LLM
        predicted_tag = classify_lead_with_llm(lead_text, API_KEY)

        print(f"Лид #{lead_id} классифицирован как: {predicted_tag}")

        classified_leads.append({
            'id': lead_id,
            'text': lead_text,
            'predicted_tag': predicted_tag
        })

    # Сохраняем результаты
    save_results(classified_leads, results_file)
    print("\nПроцесс классификации завершен.")

if __name__ == "__main__":
    main()
