import os
import json
import requests


def recognize(file_base64, file_type):
    x_folder_id = os.environ["x_folder_id"]
    jwt = os.environ["JWT"]

    headers = {"Content-Type": "application/json",
               "x-folder-id": x_folder_id,
               "x-data-logging-enabled": "true",
               "Authorization": "Bearer " + jwt}

    # Данные для отправки в теле POST-запроса
    payload = {
        "mimeType": file_type,
        "languageCodes": ["*"],
        "model": "page",
        "content": file_base64
    }

    # Отправка POST запроса
    response = requests.post("https://ocr.api.cloud.yandex.net/ocr/v1/recognizeTextAsync",
                             json=payload,
                             headers=headers)

    # Проверка статуса ответа
    if response.status_code == 200:
        try:
            id = response.json()["id"]
        except ValueError:
            print("Ошибка: Не удалось декодировать JSON.")
            return None
    else:
        print(f"Ошибка: Сервер вернул статус {response.status_code}")
        return None

    # Получение результата асинхронно
    repeat = True
    while repeat:
        response = requests.get("https://ocr.api.cloud.yandex.net/ocr/v1/getRecognition?operationId=" + id,
                                headers=headers)
        repeat = response.status_code != 200

    # Проверка статуса ответа
    if response.status_code == 200:
        try:
            # Получение и возврат текстовых блоков из JSON ответа
            json_objects = response.text.rstrip().split('\n')
            parsed_data = [json.loads(obj) for obj in json_objects]
            text = ""
            for data in parsed_data:
                text += data["result"]["textAnnotation"]["fullText"] + "\n"
            return text
        except ValueError:
            print("Ошибка: Не удалось декодировать JSON.")
            return None
    else:
        print(f"Ошибка: Сервер вернул статус {response.status_code}")
        return None
