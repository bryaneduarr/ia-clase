import cv2
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "../../../public/assets/dog.jpeg")

image = cv2.imread(image_path)

# Show Image
cv2.imshow("Image", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
