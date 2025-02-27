import cv2
import pytesseract

def extract_text(image_path):
    """Extrae texto de una carta de Pokémon con OCR optimizado."""

    # Cargar imagen
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"⚠️ ERROR: No se pudo cargar la imagen {image_path}")

    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro CLAHE para mejorar el contraste sin perder detalles
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # Aplicar un ligero desenfoque para reducir ruido sin perder texto
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # **No aplicamos umbral binario para no perder información**

    # Mostrar imagen antes del OCR
    cv2.imshow("Imagen Final para OCR", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Especificar la ruta de Tesseract manualmente
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # 🔹 Ejecutar OCR con configuración avanzada
    custom_config = r'--oem 3 --psm 11'  # Cambia a psm 4 si es necesario- funciona bien con 4 o 11
    text = pytesseract.image_to_string(gray, config=custom_config, lang="eng")

    print("Texto detectado:")
    print(text)

    return text.strip()

# Prueba con la imagen
extract_text(r"C:\Users\paula\Documents\GitHub\PRACTICAS-NBU\imagenes cartas\pikachu.jpg")
#extract_text("pikachu.jpg")