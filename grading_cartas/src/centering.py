import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def calculate_card_centering(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: No se pudo cargar la imagen.")
        return None
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Mejorar la detección de bordes
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    edges = cv2.Canny(thresh, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("No se detectó ninguna carta en la imagen.")
        return None
    
    # Filtrar contornos demasiado pequeños para evitar textos
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 5000]
    if not contours:
        print("No se encontró una carta suficientemente grande.")
        return None
    
    # Seleccionar el contorno con mayor área
    largest_contour = max(contours, key=cv2.contourArea)
    hull = cv2.convexHull(largest_contour)  # Usar contorno convexo para mejorar la detección
    x, y, w, h = cv2.boundingRect(hull)
    
    # Verificar si la forma se asemeja a una carta (relación de aspecto cercana a 2.5:3.5 o 0.7)
    aspect_ratio = w / h
    if aspect_ratio < 0.6 or aspect_ratio > 0.8:
        print("Advertencia: El contorno detectado no parece una carta. Revisar imagen.")
    
    left_margin = x
    right_margin = image.shape[1] - (x + w)
    top_margin = y
    bottom_margin = image.shape[0] - (y + h)
    
    horizontal_centering = min(left_margin, right_margin) / max(left_margin, right_margin)
    vertical_centering = min(top_margin, bottom_margin) / max(top_margin, bottom_margin)
    
    print(f"Centrado Horizontal: {horizontal_centering * 100:.2f}%")
    print(f"Centrado Vertical: {vertical_centering * 100:.2f}%")
    
    # Dibujar rectángulo sobre la carta detectada
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    # Mostrar imagen con matplotlib en lugar de cv2.imshow
    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Carta Detectada")
    plt.axis("off")
    plt.show()
    
    return horizontal_centering, vertical_centering

input_image_path = "imagenes_cartas/corviknight.jpg"  # Imagen de la carta a analizar
calculate_card_centering(input_image_path)