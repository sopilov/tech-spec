import os
import streamlit as st
import ocr.ocr as ocr
import osint.osint as osi
import nlp.nlp as nlp
import base64


def main():


    st.title("Поиск технических характеристик")
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

    st.title("Поиск технических характеристик в паспорте")
    uploaded_pdf = st.file_uploader("Выберите файл", type="pdf", accept_multiple_files=False)
    if uploaded_pdf is not None:
        pdf = base64.b64encode(uploaded_pdf.getvalue()).decode("utf-8")
    else:
        pdf = None
    ocr_button = st.button("Получить")
    if ocr_button and pdf:
        try:
            recognize_pdf = ocr.recognize_pdf(pdf_base64=pdf)
            st.markdown("Файл конвертирован в текст, выделяем главное...")
            st.write(nlp.completion(task="Выдели описание и технические характеристики из текста", text=recognize_pdf))
        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")

    uploaded_pdfs = None
    st.title("Сравнение технических характеристик в паспортах")
    uploaded_pdfs = st.file_uploader("Выберите файлы", type="pdf", accept_multiple_files=True)
    if len(uploaded_pdfs) == 2:
        pdf1 = base64.b64encode(uploaded_pdfs[0].getvalue()).decode("utf-8")
        pdf2 = base64.b64encode(uploaded_pdfs[1].getvalue()).decode("utf-8")
    else:
        pdf1 = None
        pdf2 = None
    comparison_button = st.button("Сравнить")
    if comparison_button and uploaded_pdfs:
        try:
            recognize_pdf1 = ocr.recognize_pdf(pdf_base64=pdf1)
            recognize_pdf2 = ocr.recognize_pdf(pdf_base64=pdf2)
            st.markdown("Файлы конвертированы в текст, сравниваем...")
            st.write(nlp.completion(task="Перечисли в первую очередь различия в технических характеристиках товаров из текста, затем совпадающие характеристики",
                                    text="Первый товар: \n" + recognize_pdf1 + "\nВторой товар: \n" + recognize_pdf2))
        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")
main()
