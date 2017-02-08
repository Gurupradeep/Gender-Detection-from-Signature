import cv2

from common.image_helper import get_image_bounds

image = cv2.imread('./test/samarth.jpg')

image = cv2.resize(image, None, fx=0.2, fy=0.2)

image_bounds = get_image_bounds(image, image.shape[0], image.shape[1])

bounded_image = image[image_bounds[0][0]: image_bounds[1][0], image_bounds[0][1]: image_bounds[1][1]]

cv2.imshow('Samarth', bounded_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
