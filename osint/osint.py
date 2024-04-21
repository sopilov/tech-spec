import os
import requests
import time


def send(user_request):
    token = os.environ["YA_N_TOKEN"]
    cookie = os.environ["YA_N_COOKIE"]
    url_send = os.environ["YA_N_URL_SEND"]
    url_get = os.environ["YA_N_URL_GET"]

    headers = {'Content-Type': 'application/json'}
    cookies = {'session_cookie': cookie}

    # Данные для отправки в теле POST-запроса
    payload = {
        "UserRequest": "Найди технические характеристики и описание " + user_request,
        "Token": token
    }
    # Отправка POST запроса
    response = requests.post(url_send, json=payload, headers=headers, cookies=cookies)

    # Проверка статуса ответа
    if response.status_code == 200:
        try:
            # Получение и возврат значения поля "ResponseMessageId" из JSON ответа
            response_data = response.json()
            response_message_id = response_data.get("ResponseMessageId")
        except ValueError:
            print("Ошибка: Не удалось декодировать JSON.")
            return None
    else:
        print(f"Ошибка: Сервер вернул статус {response.status_code}")
        return None

    # Данные для отправки в теле POST-запроса
    data = {
        "ResponseMessageId": response_message_id
    }

    # Пауза перед выполнением запроса, чтобы сервер успел найти данные
    time.sleep(5)

    # Отправка POST-запроса
    response = requests.post(url_get, headers=headers, cookies=cookies, json=data)

    # Проверка статуса ответа
    if response.status_code == 200:
        try:
            # Получение и возврат значения поля "TargetMarkdownText" из JSON ответа
            response_data = response.json()
            target_markdown_text = response_data.get("TargetMarkdownText")
            return "Данные из сети интернет: \n" + target_markdown_text
        except ValueError:
            print("Ошибка: Не удалось декодировать JSON.")
            return None
    else:
        print(f"Ошибка: Сервер вернул статус {response.status_code}")
        return None
