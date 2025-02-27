import cv2
import numpy as np

def calculate_grading(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detectar bordes con Canny
    edges = cv2.Canny(gray, 50, 150)
    
    # Calcular centrado (distancia del centro ideal)
    h, w = gray.shape
    center_x, center_y = w // 2, h // 2
    detected_center_x, detected_center_y = np.mean(np.where(edges > 0), axis=1)

    centering_score = max(0, 10 - abs(center_x - detected_center_x) - abs(center_y - detected_center_y))

    # Evaluar superficie (cantidad de ruido en la imagen)
    noise_score = 10 - np.sum(edges) / (w * h) * 10  # Cuanto más ruido, menor la puntuación

    # Evaluar bordes
    corners = cv2.goodFeaturesToTrack(gray, 4, 0.01, 10)
    if corners is not None:
        corner_score = min(10, len(corners) * 2.5)
    else:
        corner_score = 0

    total_score = (corner_score + centering_score + noise_score) / 3

    return {
        "corners": corner_score,
        "centering": centering_score,
        "surface": noise_score,
        "final_grade": round(total_score, 2)
    }

# Prueba con una imagen
if __name__ == "__main__":
    score = calculate_grading("pikachu.jpg")
    print("Calificación de la carta:", score)
