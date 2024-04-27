# tech-spec

Сервис по поиску технических характеристик в открытых источниках, в паспортах изделий, сравнение паспортов.

Для запуска:
```
streamlit run core.py
```

# Требуемые переменные окружения:
YA_N_COOKIE - куки из яндекс-браузера

YA_N_URL_SEND - урл отправки сообщения для поиска

YA_N_URL_GET - урл получения результата поиска

x_folder_id - folder Яндекс-облака https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id

JWT - токен Яндекс-облака https://yandex.cloud/ru/docs/iam/operations/iam-token/create


# Запуск в docker:
Соберите Docker образ
Для запуска:
```
docker build -t tech-spec-app
Для запуска:
```

Запустите контейнер
Для запуска:
```
docker run -p 8504:8504 tech-spec-app
```
