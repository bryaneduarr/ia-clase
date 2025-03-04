""" This module provides os functionality."""
import os
import smtplib
from email.message import EmailMessage
import tkinter as tk
import cv2

EMAIL_TO = "yourEmail@gmail.com"
EMAIL_FROM = "yourEmail@gmail.com"
EMAIL_PASSWORD = "password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(conteo_formas):
    """
    Sends an email to the specified email address.
    """

    total_formas = sum(conteo_formas.values())
    formas = "\n".join(
        [f"{forma}: {cantidad}" for forma, cantidad in conteo_formas.items()])
    formas = f"Formas detectadas: {total_formas}\n\n{formas}"

    msg = EmailMessage()
    msg.set_content(formas)
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print("Email sent!")
    except smtplib.SMTPException as e:
        print(f"Unexpected error: {e}")


def reporte(conteo_formas):
    """ Generar un reporte y enviarlo por correo """
    total_formas = sum(conteo_formas.values())

    window = tk.Tk()
    window.title("Reporte de formas")

    tk.Label(window, text="Formas detectadas").pack()

    for forma, cantidad in conteo_formas.items():
        tk.Label(window, text=f"{forma}: {cantidad}").pack()

    tk.Label(window, text=f"Total de formas: {total_formas}").pack()

    # Enviar un correo con el total de las formas
    send_to_mail = tk.Button(
        window, text="Enviar por correo", command=lambda: send_email(conteo_formas))
    send_to_mail.pack()

    window.mainloop()


def detectar_formas(img):
    """
    Detecta formas en una imagen.
    """
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque gaussiano para reducir el ruido
    desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)

    # Realizar detección de bordes con Canny
    bordes = cv2.Canny(desenfoque, 50, 150)

    # Encontrar contornos en la imagen de bordes
    contornos, _ = cv2.findContours(
        bordes.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contar_formas = {"Triangulo": 0,
                     "Cuadrado o Rectangulo": 0, "Pentagono": 0, "Circulo": 0}

    for contorno in contornos:
        # Aproximar la forma del contorno actual
        perimetro = cv2.arcLength(contorno, True)
        aprox = cv2.approxPolyDP(contorno, 0.03 * perimetro, True)

        # Determinar el número de lados de la forma aproximada
        lados = len(aprox)

        # Definir el nombre de la forma en base a su número de lados
        if lados == 3:
            forma = "Triangulo"
        elif lados == 4:
            forma = "Cuadrado o Rectangulo"
        elif lados == 5:
            forma = "Pentagono"
        else:
            forma = "Circulo"

        contar_formas[forma] += 1

        # Dibujar el contorno de la forma y mostrar su nombre
        cv2.drawContours(img, [aprox], -1, (0, 255, 0), 2)
        cv2.putText(img, forma, (aprox.ravel()[0], aprox.ravel()[
                    1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Declarar el total de formas encontradas.
    total_formas = sum(contar_formas.values())
    y_offset = 20

    # Iterar por cada forma y encontrar el total de veces que aparece.
    for forma, cantidad in contar_formas.items():
        cv2.putText(img, f"{forma}: {cantidad}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        y_offset += 30

    # Mostrar el total de formas encontradas
    cv2.putText(img, f"Total Formas: {total_formas}", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Generar reporte con la opcion de mandar al correo.
    reporte(contar_formas)

    # Mostrar la imagen con las formas detectadas
    cv2.imshow("Formas detectadas", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Cargar la imagen
current_dir = os.path.dirname(os.path.abspath(__file__))
public_path = os.path.join(current_dir, "../../../public/")
imagen = cv2.imread(os.path.join(public_path, "assets", "geometric-forms.jpg"))

# Llamar a la función para detectar formas
detectar_formas(imagen)
