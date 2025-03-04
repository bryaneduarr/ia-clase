""" This module provides os functionality"""
import os
import sys
from email.message import EmailMessage
import smtplib
import cv2

SEND_MAIL = "ON"
EMAIL_TO = "yourEmail@gmail.com"
EMAIL_FROM = "yourEmail@gmail.com"
EMAIL_PASSWORD = "yourPassword"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email():
    """
    Sends an email to the specified email address.
    """

    msg = EmailMessage()
    msg.set_content(SEND_MAIL)
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


# General paths to follow.
current_dir = os.path.dirname(os.path.abspath(__file__))
public_path = os.path.join(current_dir, "../../../public/")
data_path = os.path.join(public_path, "data")
model_path = os.path.join(data_path, "eigen-face-model.xml")
PERSON_NAME = "rosy"

# People list on the 'data/' directory.
people_list = os.listdir(data_path)
print(f"People list: {people_list}")

# Initializing face recognizer.
model = cv2.face.EigenFaceRecognizer_create()
# Leyendo el modelo
model.read(model_path)

# Path to the Haar cascade file.
haar_path = os.path.join(
    public_path, "data", PERSON_NAME, "haarcascade_frontalface_default.xml"
)
faceClassif = cv2.CascadeClassifier(haar_path)

# Validate if the Haar cascade file exists.
if not os.path.exists(haar_path):
    print("error: Haar cascade file not found.", haar_path)
    sys.exit(1)

# Path to the video file.
video_path = os.path.join(public_path, "assets", "smile.mp4")
cap = cv2.VideoCapture(video_path)

# Validate if the video file exists.
if not cap.isOpened:
    print("error: Can not open video.")
    sys.exit(1)

# Send the email
send_email()

while True:
    ret, frame = cap.read()

    # Validate if the video is finished.
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Convert the frame to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aux_frame = gray.copy()

    # Detect faces in the frame as rectanglees.
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in faces:
        # Region of interest are drawn in the grayscale image.
        face = aux_frame[y: y + h, x: x + w]
        # Resize the face to 150x150 pixels.
        face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)

        color = (0, 255, 0) if SEND_MAIL == "ON" else (0, 0, 255)

        if SEND_MAIL == "ON":
            # Returns a predicted label of confidence
            result = model.predict(face)
            LABEL = "Known" if result[1] < 5700 else "Unknown"
        else:
            LABEL = "Unknown"

        # Print if the face is known on top of the image.
        cv2.putText(
            frame,
            LABEL,
            (x, y - 25),
            2,
            1.1,
            color,
            1,
            cv2.LINE_AA,
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.imshow("Frame", frame)

    # Exit the loop if the user presses the ESC key.
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
