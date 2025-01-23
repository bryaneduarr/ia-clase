import cv2
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "../../assets/dog.jpeg")

image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Show the grayscale image
cv2.imshow("Grayscale Image", gray_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
