import streamlit as st
from preprocess import preprocess_image
from ocr import extract_text
from grading import calculate_grading

st.title("Sistema de Grading de Cartas")

uploaded_file = st.file_uploader("Sube una imagen de la carta", type=["jpg", "png"])

if uploaded_file:
    # Guardar imagen temporal
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Procesar imagen
    text = extract_text("temp.jpg")
    grading = calculate_grading("temp.jpg")

    # Mostrar resultados
    st.image("temp.jpg", caption="Carta Analizada")
    st.write(f"Texto Detectado: {text}")
    st.write(f"Calificación: {grading}")
