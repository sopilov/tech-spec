import os
import streamlit as st
import ocr.ocr as ocr
import osint.osint as osi
import nlp.nlp as nlp
import base64
import re


def main():

    # osint
    st.title("Поиск технических характеристик в открытых источниках")
    text = st.text_input("Введите полное наименование товара")
    osint_button = st.button("Поиск")
    if osint_button and text:
        try:
            # выводим результат
            st.markdown("**Данные из сети интернет:**")
            st.write(osi.send(text))
        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")

    # ocr + nlp
    st.title("Поиск технических характеристик в паспорте")
    uploaded_files = st.file_uploader("Выберите файлы",
                                      type=["jpeg", "jpg", "png", "pdf"],
                                      accept_multiple_files=True,
                                      key="file_uploader_1")
    base64_files = {}
    recognized_text = ""
    search_task = "Выдели описание и технические характеристики"
    json_task = "Предоставь данные в форме json, json должен быть валиден для десериализации"
    for uploaded_file in uploaded_files:
        base64_files[base64.b64encode(uploaded_file.getvalue()).decode("utf-8")] = uploaded_file.type
    ocr_button = st.button("Получить")
    if ocr_button and len(uploaded_files) > 0:
        try:
            for key in base64_files.keys():
                recognized_text += ocr.recognize(file_base64=key, file_type=base64_files[key]) + "\n"
            compl_text = nlp.completion(task=search_task, text=recognized_text)
            json_text = fix_json_quotes(nlp.completion(task=json_task, text=compl_text))
            st.write(compl_text + "\n" + json_text)
        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")

    # ocr + nlp
    st.title("Сравнение технических характеристик в паспортах")
    uploaded_pdfs = st.file_uploader("Выберите файлы",
                                     type=["jpeg", "jpg", "png", "pdf"],
                                     accept_multiple_files=True,
                                     key="file_uploader_2")
    comparison_button = st.button("Сравнить")
    if comparison_button and len(uploaded_pdfs) == 2:
        try:
            file1 = uploaded_pdfs[0]
            file2 = uploaded_pdfs[1]
            recognize_text1 = ocr.recognize(file_base64=base64.b64encode(file1.getvalue()).decode("utf-8"), file_type=file1.type)
            recognize_text2 = ocr.recognize(file_base64=base64.b64encode(file2.getvalue()).decode("utf-8"), file_type=file2.type)
            st.markdown("Файлы конвертированы в текст, сравниваем...")
            st.write(nlp.completion(
                task="Перечисли в первую очередь различия в технических характеристиках товаров из текста, затем совпадающие характеристики",
                text="Первый товар: \n" + recognize_text1 + "\nВторой товар: \n" + recognize_text2))
        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")


def fix_json_quotes(text):
    # Предполагаем, что входной текст - это строка JSON без кавычек у ключей и значений там, где они должны быть
    # Регулярное выражение для поиска ключей и значений без кавычек
    pattern = r'\b(\w+)\b(?=:)'  # Ищем слова перед двоеточием (ключи)
    fixed_keys = re.sub(pattern, r'"\1"', text)

    # Теперь исправляем значения, если они не заключены в кавычки
    # Ищем последовательности после двоеточия, которые не начинаются на кавычку или цифру (простые строки без кавычек)
    pattern_values = r'(?<=:)\s*(?=\S)([\w\s\-\.]+)'
    fixed_values = re.sub(pattern_values, r'"\1"', fixed_keys)
    return fixed_values


main()
