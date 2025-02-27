# PRACTICAS-NBU
# Pasos para realizar el proyecto
 - Paso 1: Cargar la Imagen de la Carta
  📌 Herramientas: OpenCV
  📌 Tareas:
  Convertir la imagen a escala de grises.
  Mejorar el contraste para detectar bordes.
  Identificar los contornos de la carta en la imagen.
  Recortar y alinear la carta.
- Paso 2: Extraer Texto con OCR
  📌 Herramientas: Tesseract OCR
  📌 Tareas:
  Extraer texto de la imagen (nombre de la carta, serie, número, etc.).
  Filtrar y limpiar los datos para evitar errores de OCR.
  Comparar con una base de datos de cartas existentes.
- Paso 3: Identificación de Características de la Carta
  📌 Herramientas: OpenCV
  📌 Tareas:
  Detección de bordes y esquinas.
  Detección de centrado de la imagen.
  Evaluación de la superficie en busca de defectos.
- Paso 4: Aplicar Modelo de Machine Learning para Grading
  📌 Herramientas: CNN (Red Neuronal Convolucional)
  📌 Tareas:
  Entrenar un modelo con imágenes de cartas bien calificadas y defectuosas.
  Clasificar la carta según su calidad en diferentes categorías (esquinas, bordes, centrado, superficie).
  Asignar un puntaje basado en reglas predefinidas.
- Paso 5: Interfaz Gráfica para Mostrar los Resultados
  📌 Herramientas: Streamlit / Flask
  📌 Tareas:
  Permitir al usuario cargar una imagen.
  Mostrar los puntajes de cada aspecto de la carta.
  Explicar cómo se llegó a la calificación.
  Comparar con otras cartas similares y estimar su valor.
