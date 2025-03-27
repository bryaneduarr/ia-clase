"""Modulos"""
import os
import math
import numpy as np
import cv2


def detect_circles(image):
    """Detectar circulos en una imagen utilizando el metodo de Hough."""

    # Crear una copia de la imagen.
    output_image = image.copy()

    # Convertir a imagen gris.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque gaussiano para reducir el ruido y mejorar la detección.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detectar circulos utilizando el metodo de Hough.
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 50,
                               param1=100, param2=30, minRadius=10, maxRadius=100)

    # Si se detectan circulos, dibujar los circulos en la imagen de salida.
    if circles is not None:
        # Convertir las coordenadas de los circulos a enteros.
        circles = np.uint16(np.around(circles))

        # Dibjujar los circulos en la imagen de salida.
        for circle in circles[0, :]:
            # Dibujar el contorno del circulo.
            cv2.circle(
                output_image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            # Dibujar el centro del circulo.
            cv2.circle(output_image, (circle[0], circle[1]), 2, (0, 0, 255), 3)

    return circles, output_image


def calculate_distance(circles, pixels_per_cm):
    """Calcular la distancia entre dos circulos."""

    # Verificar que se detectaron al menos 2 circulos.
    if circles is None or circles.shape[1] < 2:
        return 0

    # Obtener las coordenadas de los dos circulos y los pasamos a flotantes.
    x1, y1 = float(circles[0, 0, 0]), float(circles[0, 0, 1])
    x2, y2 = float(circles[0, 1, 0]), float(circles[0, 1, 1])

    # Calcular la diferencia entre las coordenadas "x" y "y" de los dos circulos.
    dx = x2 - x1
    dy = y2 - y1

    # Calcular la distancia entre los dos circulos utilizando la formula de la distancia euclidiana.
    distance_pixels = math.sqrt(dx**2 + dy**2)

    # Convertir la distancia de píxeles a centímetros
    distance_cm = distance_pixels / pixels_per_cm

    return distance_cm


def main():
    """Funcion principal para detectar la distancia entre dos circulos."""

    # Ruta de la imagen.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    public_path = os.path.join(current_dir, "../../../public/")
    image_path = os.path.join(public_path, "assets/distance.png")

    # Verificar si la imagen existe.
    if not os.path.exists(image_path):
        print(f"La imagen no existe en la ubicacion: {image_path}.")
        return

    # Leer la imagen.
    image = cv2.imread(image_path)

    # Verificar si la imagen se leyo correctamente.
    if image is None:
        print(f"La imagen no se puede leer en la ubicacion: {image_path}.")
        return

    # Detectar los circulos en la imagen.
    circles, output_image = detect_circles(image)

    # Verificar que los circulos detectados sean al menos 2.
    if circles is not None and circles.shape[1] >= 2:
        # Calcular la distancia entre los circulos.
        # Ajustar el factor de conversión según la imagen (10 píxeles = 1 cm es un ejemplo)
        pixels_per_cm = 10.0
        distance_cm = calculate_distance(
            circles, pixels_per_cm)

        # Crear un texto con la distancia.
        text = f"Distancia: {distance_cm:.2f} cm"

        # Añadir el texto a la imagen de salida en la parte superiror izquierda.
        cv2.putText(output_image, text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Imprimir en consola la distancia entre los circulos.
        print(
            f"La distancia entre los dos circulos es: {distance_cm:.2f} cm")

        # Mostrar la imagen de salida con los circulos detectados y
        # la distancia utilizando la libreria CV2.
        cv2.imshow("Distancia entre circulos", output_image)

        # Esperar a que se presione una tecla y luego cerrar todas las ventanas
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        # Si no se detectaron circulos imprimir un mensaje de error.
        print("No se pudieron detectar dos circulos en la imagen.")


if __name__ == "__main__":
    main()
