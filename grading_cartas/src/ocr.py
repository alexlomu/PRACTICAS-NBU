import pytesseract
import cv2

def extract_text(image_path):
    # Cargar imagen y convertir a escala de grises
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Usar Tesseract OCR para extraer texto
    text = pytesseract.image_to_string(gray, lang="eng")
    
    return text.strip()

# Prueba con una imagen
if __name__ == "__main__":
    text = extract_text("pikachu.jpg")
    print("Texto extraído:", text)
