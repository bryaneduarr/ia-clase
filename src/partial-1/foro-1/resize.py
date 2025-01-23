import cv2
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "../../assets/dog.jpeg")

image = cv2.imread(image_path)

# Resize the image to half its original dimensions
height, width = image.shape[:2]
resized_image = cv2.resize(image, (width // 2, height // 2))

# Show the resized image
cv2.imshow("Resized Image", resized_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
