import cv2
import pytesseract
from PIL import Image
import os
import difflib
import re

def classify_card(image_path):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    if not os.path.exists(image_path):
        print(f"Error: La imagen {image_path} no se encuentra.")
        return
    
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    temp_image = "temp.png"
    cv2.imwrite(temp_image, gray)
    
    try:
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(Image.open(temp_image), lang='eng', config=custom_config)
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract no está instalado o no está en la variable PATH.")
        return
    
    # Limpiar el texto extraído (eliminar caracteres especiales y convertir a minúsculas)
    extracted_text = re.sub(r'[^a-zA-Z0-9\s]', '', extracted_text).lower()
    
    categories = {
        "Pokémon": ["pokemon", "pikachu", "charizard", "pokeball"],
        "Dragon Ball": ["dragon ball", "goku", "vegeta", "kamehameha"],
        "LaLiga": ["laliga", "barcelona", "real madrid", "messi"],
        "Yu-Gi-Oh!": ["yu-gi-oh", "blue-eyes", "dark magician"],
        "One Piece": ["one piece", "luffy", "zoro", "nami"],
        "Disney Lorcana": ["disney lorcana", "mickey", "donald", "goofy"],
        "Star Wars Unlimited": ["star wars unlimited", "vader", "jedi", "sith"],
        "Flesh and Blood": ["flesh blood", "fab", "arcane", "warrior"],
        "Digimon Card Game": ["digimon", "agumon", "gabumon", "tamer"],
        "Vanguard": ["vanguard", "blaster", "overdress", "clan"],
        "Weiß Schwarz": ["weis schwarz", "anime", "waifu", "shiny"],
        "Battle Spirits Saga": ["battle spirits saga", "core", "spirit", "burst"],
        "Final Fantasy": ["final fantasy", "cloud", "sephiroth", "chocobo"],
        "Force of Will": ["force of will", "fow", "ruler", "magic stone"],
        "World of Warcraft": ["world of warcraft", "wow", "horde", "alliance"],
        "Star Wars Destiny": ["star wars destiny", "force", "blaster", "droid"],
        "Dragon Borne": ["dragon borne", "ember", "storm", "ally"],
        "Little Pony": ["little pony", "mlp", "twilight sparkle", "friendship"],
        "Spoils": ["spoils", "greed", "rogue", "warrior"]
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

image_path = "pikachu2.jpg"
classify_card(image_path)