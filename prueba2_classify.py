import cv2
import pytesseract
import easyocr
from PIL import Image
import os
import difflib
import numpy as np
import re

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    
    temp_image = "temp.png"
    cv2.imwrite(temp_image, gray)
    return temp_image

def extract_text_tesseract(image_path):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    temp_image = preprocess_image(image_path)
    custom_config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(Image.open(temp_image), lang='eng', config=custom_config)
    return re.sub(r'[^a-zA-Z0-9\s]', '', extracted_text).lower()

def extract_text_easyocr(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    return " ".join([res[1].lower() for res in results])

def classify_card(image_path, use_easyocr=False):
    if not os.path.exists(image_path):
        print(f"Error: La imagen {image_path} no se encuentra.")
        return
    
    extracted_text = extract_text_easyocr(image_path) if use_easyocr else extract_text_tesseract(image_path)
    
    categories = {
        "Pokémon": ["pokemon"],
        "Dragon Ball": ["dragon ball card game"],
        "LaLiga": ["laliga", "panini"],
        "Yu-Gi-Oh!": ["yu-gi-oh"],
        "One Piece": ["one piece"],
        "Disney Lorcana": ["disney lorcana"],
        "Star Wars Unlimited": ["star wars unlimited"],
        "Flesh and Blood": ["flesh blood"],
        "Digimon Card Game": ["digimon"],
        "Vanguard": ["vanguard"],
        "Weiß Schwarz": ["weis schwarz"],
        "Battle Spirits Saga": ["battle spirits saga"],
        "Final Fantasy": ["final fantasy"],
        "Force of Will": ["force of will"],
        "World of Warcraft": ["world of warcraft", "wow"],
        "Star Wars Destiny": ["star wars destiny"],
        "Dragon Borne": ["dragon borne"],
        "Little Pony": ["little pony"],
        "Spoils": ["spoils"]
    }
    
    detected_categories = []
    words_in_text = extracted_text.split()
    
    def find_similar_matches(word_list, keywords, threshold=0.7):
        for word in word_list:
            matches = difflib.get_close_matches(word, keywords, n=1, cutoff=threshold)
            if matches:
                return True
        return False
    
    for category, keywords in categories.items():
        if find_similar_matches(words_in_text, keywords):
            detected_categories.append(category)
    
    print("Texto extraído:")
    print(extracted_text)
    
    if detected_categories:
        print("Categoría detectada:", ", ".join(detected_categories))
    else:
        print("No se pudo clasificar la carta.")

# Prueba con una imagen y opción de usar EasyOCR en lugar de Tesseract
image_path = "imagenes cartas/dragonball_detras.jpg"
classify_card(image_path, use_easyocr=True)