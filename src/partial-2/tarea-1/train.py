""" This module provides os functionality"""
import os
import numpy as np
import cv2

# General paths to follow.
current_dir = os.path.dirname(os.path.abspath(__file__))
public_path = os.path.join(current_dir, "../../../public/")
data_path = os.path.join(public_path, "data")

# People list on the 'data/' directory.
people_list = os.listdir(data_path)
print(f"People list: {people_list}")

facesData = []
labels = []
LABEL = 0

for name_dir in people_list:
    person_path = os.path.join(data_path, name_dir)
    print(f"Reading images from: {person_path}...")

    for file_name in os.listdir(person_path):
        file_path = os.path.join(person_path, file_name)

        if file_name == "haarcascade_frontalface_default.xml":
            print("Skipping: haarcascade_frontalface_default.xml")
            continue

        print(f"Face image: {file_path}")

        # Reading image in grayscale.
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Append image and label to the lists.
        facesData.append(image)
        labels.append(LABEL)

        cv2.imshow("Image", image)
        cv2.waitKey(10)

    LABEL += 1

# Print label statistics after reading images.
print("Labels: ", labels)
print("Number of labels 0: ", np.count_nonzero(np.array(labels) == 0))
print("Number of labels 1: ", np.count_nonzero(np.array(labels) == 1))

# Initializing face recognizer and training it.
face_recognizer = cv2.face.EigenFaceRecognizer_create()
print("Training...")
face_recognizer.train(facesData, np.array(labels))

# Saving the model
model_path = os.path.join(public_path, "data", "eigen-face-model.xml")
face_recognizer.write(model_path)
print(f"Successfully saved model to: {model_path}")
