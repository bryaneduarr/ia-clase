import imutils
import time
import cv2
import os

# General path to the public folder.
current_dir = os.path.dirname(os.path.abspath(__file__))
public_path = os.path.join(current_dir, "../../../public/")
person_name = 'rosy'

# Path to data folder.
data_name_path = os.path.join(public_path, "data", person_name)

# Validate if the data folder exists and create it if it does not.
if not os.path.exists(data_name_path):
    os.makedirs(data_name_path)
    print('Folder created: ', data_name_path)

# Path to the Haar cascade file.
haar_path = os.path.join(
    public_path, "data", person_name, "haarcascade_frontalface_default.xml")
faceClassif = cv2.CascadeClassifier(haar_path)

# Validate if the Haar cascade file exists.
if not os.path.exists(haar_path):
    print("error: Haar cascade file not found.", haar_path)
    exit(1)

# Path to the video file.
video_path = os.path.join(public_path, "assets", "smile.mp4")
cap = cv2.VideoCapture(video_path)

# Validate if the video file exists.
if not cap.isOpened:
    print("error: Can not open video.")
    exit(1)

count = 0

while True:
    ret, frame = cap.read()

    # Validate if the video is finished.
    if not ret:
        print("Video finished.")
        break

    # Resize the frame.
    frame = imutils.resize(frame, width=640)
    # Convert the frame to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Create a copy of the frame.
    auxFrame = frame.copy()

    # Detect faces in the frame.
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
    # Print the number of faces detected.
    print(f"Frame {count}: Detected {len(faces)} face(s).")

    for (x, y, w, h) in faces:
        # Draw a rectangle around the face.
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

        # Save the face in a file.
        face_filename = os.path.join(
            data_name_path, f"face_{count}_{int(time.time())}.jpg")
        cv2.imwrite(face_filename, rostro)

        count = count + 1

    cv2.imshow('Detected Faces', frame)

    # Exit the loop if the user presses the ESC key or the count is greater than 300.
    k = cv2.waitKey(1)
    if k == 27 or count >= 300:
        break

cap.release()
cv2.destroyAllWindows()
