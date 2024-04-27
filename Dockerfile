# Используйте официальный образ Python 3.9
FROM python:3.9-slim

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файлы requirements.txt в рабочую директорию
COPY requirements.txt .

# Установите зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте остальные файлы проекта в рабочую директорию
COPY . .

# Команда для запуска приложения
CMD ["streamlit", "run", "core.py"]

# Откройте порт 8501 для доступа к Streamlit
EXPOSE 8504
