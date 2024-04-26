import os
import requests


def completion(task, text):
    x_folder_id = os.environ["x_folder_id"]
    jwt = os.environ["JWT"]

    headers = {"Content-Type": "application/json",
               "x-folder-id": x_folder_id,
               "Authorization": "Bearer " + jwt}

    # Данные для отправки в теле POST-запроса
    payload = {
        "modelUri": "gpt://" + x_folder_id + "/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": task
            },
            {
                "role": "user",
                "text": text
            }
        ]
    }

    # Отправка POST запроса
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                             json=payload,
                             headers=headers)

    # Проверка статуса ответа
    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data["result"]["alternatives"][0]["message"]["text"]
        except ValueError:
            print("Ошибка: Не удалось декодировать JSON.")
            return None
    else:
        print(f"Ошибка: Сервер вернул статус {response.status_code}")
        return None
