import base64

import streamlit as st
from transformers import pipeline, AutoModel


def main():
    # загружаем предварительно обученную модель
    model = pipeline("image-to-text", model="kha-white/manga-ocr-base")
    created_button = False


    st.title("Конвертация картинки в текст")

    # форма для загрузки картинки
    uploaded_file = st.file_uploader("Выберите файл", type="jpg", accept_multiple_files=False)
    if uploaded_file is not None:
        # чтение из файла
        img = uploaded_file.read()
        # выводим картинку
        st.image(img)
        # выводим кнопку "Конвертировать"
        created_button = st.button("Конвертировать")

    if created_button and img:
        try:
            # выводим результат
            st.markdown("**Результат:**")
            st.write(model(img))
        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")


main()
