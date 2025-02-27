import cv2
import numpy as np

def preprocess_image(image_path):
    # Cargar imagen
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar filtros para mejorar bordes
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No se detectaron cartas en la imagen.")

    # Ordenar contornos por área y obtener el más grande (suponemos que es la carta)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    card_contour = contours[0]

    # Aproximar el contorno a una forma cuadrada
    epsilon = 0.02 * cv2.arcLength(card_contour, True)
    approx = cv2.approxPolyDP(card_contour, epsilon, True)

    # Si tiene 4 puntos, es la carta
    if len(approx) == 4:
        points = approx.reshape(4, 2)
        return points
    else:
        raise ValueError("No se detectó una forma cuadrada de la carta.")

# Prueba con una imagen
if __name__ == "__main__":
    points = preprocess_image("../data/carta.jpg")
    print("Puntos detectados:", points)
