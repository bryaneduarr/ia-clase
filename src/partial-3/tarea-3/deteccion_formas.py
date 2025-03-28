"""Importacion de las librerias necesarias"""
from tkinter import filedialog, messagebox
import tkinter as tk
import subprocess
import os
import cv2
import numpy as np


def procesar_imagen(imagen_path):
    """
    Procesar la imagen para detectar contornos.
    """
    img = cv2.imread(imagen_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges


def calcular_lados_triangulo(approx):
    """
    Calcula los lados de un triángulo dado sus vertices.
    """
    lados = []
    for i in range(3):
        p1 = approx[i][0]
        p2 = approx[(i+1) % 3][0]
        lado = np.linalg.norm(p1 - p2)
        lados.append(lado)
    return lados


def determinar_triangulo(lados):
    """
    Determina el tipo de triangulo basado en sus lados.
    """
    a, b, c = sorted(lados)
    perimetro = sum(lados)

    if np.isclose(a, b) and np.isclose(b, c):
        tipo = "Equilatero"
    elif np.isclose(a, b) or np.isclose(b, c) or np.isclose(a, c):
        tipo = "Isosceles"
    else:
        tipo = "Escaleno"

    return tipo, perimetro


def detectar_triangulos(imagen_path):
    """
    Funcion para detectar triangulos en una imagen y guardar los 
    resultados en una base de datos.
    """
    edges = procesar_imagen(imagen_path)
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 3:  # Verificamos que tenga 3 lados
            lados = calcular_lados_triangulo(approx)
            tipo, perimetro = determinar_triangulo(lados)
            guardar_en_bd(tipo, 3, perimetro)


def guardar_en_bd(tipo, num_lados, perimetro):
    """
    Funcion para guardar en la base de datos usando shell script.
    """
    # Obtener la ruta del archivo shell script.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "guardar_triangulo.sh")

    # Hacer el script ejecutable.
    subprocess.run(f"chmod +x {script_path}", shell=True, check=False)

    comando = f"{script_path} '{tipo}' {num_lados} {perimetro}"
    subprocess.run(comando, shell=True, check=False)


def cargar_imagen():
    """
    Funcion para cargar una imagen.
    """
    archivo = filedialog.askopenfilename(
        filetypes=[("Imagenes", "*.jpg;*.png;*.jpeg")])
    if archivo:
        detectar_triangulos(archivo)
        messagebox.showinfo(
            "Resultados", "Los triangulos han sido detectados y almacenados en la base de datos.")


# Interfaz grafica con Tkinter.
root = tk.Tk()
root.title("Deteccion de Triangulos")

btn_cargar = tk.Button(root, text="Cargar Imagen", command=cargar_imagen)
btn_cargar.pack(pady=20)

root.mainloop()
