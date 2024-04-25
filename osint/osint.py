import os
import requests


def send(user_request):
    cookie = os.environ["YA_N_COOKIE"]
    url_send = os.environ["YA_N_URL_SEND"]
    url_get = os.environ["YA_N_URL_GET"]

    headers = {'Content-Type': 'application/json'}
    cookies = {'session_cookie': cookie}

    # Данные для отправки в теле POST-запроса
    payload = {
        "UserRequest": "Найди технические характеристики и описание " + user_request
    }
    # Отправка POST запроса
    response = requests.post(url_send, json=payload, headers=headers, cookies=cookies)

    # Проверка статуса ответа
    if response.status_code == 200:
        try:
            # Получение значения поля "ResponseMessageId" из JSON ответа
            response_data = response.json()
            print(response_data["ResponseStatus"]["LimitsInfo"]["CommentByLang"]["ru"])
            response_message_id = response_data["ResponseMessageId"]
        except ValueError:
            print("Ошибка: Не удалось декодировать JSON.")
            return None
    else:
        print(f"Ошибка: Сервер вернул статус {response.status_code}")
        return None

    data = {
        "ResponseMessageId": response_message_id
    }

    # Отправка POST-запроса пока не придет флаг True
    complete = False
    while not complete:
        response = requests.post(url_get, headers=headers, cookies=cookies, json=data)
        response_data = response.json()
        complete = response_data["IsCompleteResults"]

    # Проверка статуса ответа
    if response.status_code == 200:
        try:
            # Получение и возврат значения поля "TargetMarkdownText" из JSON ответа
            response_data = response.json()
            target_markdown_text = response_data["TargetMarkdownText"]
            links = ""
            for element in response_data["LinksData"]:
                links += "\n\n" + str(element["Num"]) + ". " + element["FullUrl"]
            return ("Данные из сети интернет: \n\n" + target_markdown_text
                    + "\n\nИспользуемые источники:" + links)
        except ValueError:
            print("Ошибка: Не удалось декодировать JSON.")
            return None
    else:
        print(f"Ошибка: Сервер вернул статус {response.status_code}")
        return None
