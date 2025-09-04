import json
import pandas as pd

def load_leads(file_path):
    """
    Загружает тестовые данные о лидах из JSON-файла.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return []

def save_results(data, file_path):
    """
    Сохраняет результаты классификации в CSV-файл.
    """
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Результаты сохранены в файл: {file_path}")
