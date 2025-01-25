import cv2
import os

# General paths to follow.
current_dir = os.path.dirname(os.path.abspath(__file__))
public_path = os.path.join(current_dir, "../../../public/")
data_path = os.path.join(public_path, "data")
model_path = os.path.join(data_path, "eigen-face-model.xml")
person_name = "rosy"

# People list on the 'data/' directory.
people_list = os.listdir(data_path)
print(f"People list: {people_list}")

# Initializing face recognizer.
model = cv2.face.EigenFaceRecognizer_create()
# Leyendo el modelo
model.read(model_path)

# Path to the Haar cascade file.
haar_path = os.path.join(
    public_path, "data", person_name, "haarcascade_frontalface_default.xml"
)
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

while True:
    ret, frame = cap.read()

    # Validate if the video is finished.
    if not ret:
        print("Video finished.")
        break

    # Convert the frame to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aux_frame = gray.copy()

    # Detect faces in the frame as rectanglees.
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in faces:
        # Region of interest are drawn in the grayscale image.
        face = aux_frame[y : y + h, x : x + w]
        # Resize the face to 150x150 pixels.
        face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
        # Returns a predicted label of confidence.
        result = model.predict(face)

        # Print if the face is known on top of the image.
        cv2.putText(
            frame,
            "{}".format(result),
            (x, y - 5),
            1,
            1.3,
            (255, 255, 0),
            1,
            cv2.LINE_AA,
        )

        if result[1] < 5700:
            # Print above the rectangle the name of the person recognized in green.
            cv2.putText(
                frame,
                "Known"(x, y - 25),
                2,
                1.1,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )

            # Print the frame in green.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("Known")
        else:
            # Print above the rectangle "Intruder".
            cv2.putText(
                frame, "Unkown", (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA
            )
            # Print the frame in red.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            print("Unkown")

    cv2.imshow("Frame", frame)

    # Exit the loop if the user presses the ESC key.
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
