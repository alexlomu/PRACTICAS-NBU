import cv2 
import numpy as np
import os

def load_reference_images(reference_folder):
    reference_images = {}
    for filename in os.listdir(reference_folder):
        if filename.endswith(('.jpg', '.png', '.jpeg', '.JPG')):
            brand_name = os.path.splitext(filename)[0]  # Usa el nombre del archivo como la marca
            image_path = os.path.join(reference_folder, filename)
            reference_images[brand_name] = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return reference_images

def detect_brand(input_image_path, reference_folder):
    input_image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    if input_image is None:
        print("Error: No se pudo cargar la imagen de entrada.")
        return None
    
    reference_images = load_reference_images(reference_folder)
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(input_image, None)
    
    if descriptors1 is None:
        print("Error: No se encontraron características en la imagen de entrada.")
        return None
    
    best_match = None
    best_score = 0
    
    for brand, ref_image in reference_images.items():
        keypoints2, descriptors2 = orb.detectAndCompute(ref_image, None)
        
        if descriptors2 is None:
            continue
        
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key=lambda x: x.distance)
        score = len(matches)
        
        if score > best_score:
            best_score = score
            best_match = brand
    
    if best_match:
        print(f"La carta pertenece a la marca: {best_match}")
        
        # Preguntar al usuario si la marca detectada es correcta
        respuesta = input(f"¿Es correcta la marca detectada ({best_match})? (sí/no): ").strip().lower()
        if respuesta == "no":
            print("Por favor, introduce otra imágen de la carta.")
        else:
            print("Marca confirmada correctamente.")
    else:
        print("No se encontró una coincidencia clara.")
    
    return best_match

# Prueba con una imagen
reference_folder = "reference_images"  # Carpeta con imágenes de referencia
input_image_path = "imagenes_cartas/lorcana_detras2.jpg"  # Imagen de la carta a analizar
detect_brand(input_image_path, reference_folder)
