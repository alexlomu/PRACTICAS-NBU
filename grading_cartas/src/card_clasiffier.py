import cv2
import pytesseract
from PIL import Image
import streamlit as st
import numpy as np

# Lista de palabras clave por tipo de carta
CATEGORIES = {
    "Pokemon": ["Pokémon", "Pokeball", "Energy", "Tatsugiri"],
    "Fútbol": ["Panini", "Megacracks", "World Class", "Ronaldo", "Vinicius", "Beckham"],
    "Dragon Ball": ["Dragon Ball", "Saiyan", "Super Card Game", "Power of the Tree"],
    "Otros": ["Grading", "Corners", "Edges"]
}

class CardGrader:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"No se pudo cargar la imagen en la ruta: {image_path}")
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    
    def extract_text(self):
        processed_img = cv2.adaptiveThreshold(self.gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return pytesseract.image_to_string(processed_img, lang="eng+spa")
    
    def classify_card(self):
        text = self.extract_text()
        for category, keywords in CATEGORIES.items():
            if any(keyword.lower() in text.lower() for keyword in keywords):
                return category
        return "Desconocido"
    
    def grade_card(self):
        """Asigna una calificación a la carta basada en su tipo."""
        card_type = self.classify_card()
        grading_scale = {
            "Pokemon": np.random.uniform(8.0, 10.0),
            "Fútbol": np.random.uniform(7.5, 9.5),
            "Dragon Ball": np.random.uniform(8.0, 9.8),
            "Otros": np.random.uniform(6.0, 9.0)
        }
        return grading_scale.get(card_type, np.random.uniform(5.0, 9.0))

def identify_card_type(text):
    """Identifica el tipo de carta basado en palabras clave."""
    for category, keywords in CATEGORIES.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return category
    return "Desconocido"

def process_image(image_path):
    """Aplica OCR a la imagen y devuelve el texto extraído."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    text = pytesseract.image_to_string(processed_img, lang="eng+spa")
    return text

# Interfaz con Streamlit
st.title("Identificador de Cartas")
uploaded_file = st.file_uploader("Sube una imagen de la carta", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)
    
    # Guardar temporalmente la imagen y procesarla
    image_path = "temp_card.jpg"
    image.save(image_path)
    
    grader = CardGrader(image_path)
    card_type = grader.classify_card()
    card_grade = grader.grade_card()
    
    st.write(f"Tipo de carta detectado: **{card_type}**")
    st.write(f"Calificación asignada: **{card_grade:.1f}/10**")
