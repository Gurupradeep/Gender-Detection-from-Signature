import cv2

from common.image_helper import get_image_bounds

THRESHOLD = 100
MAX_VALUE = 255
MIN_VALUE = 0

image = cv2.imread('./test/samarth.jpg')

image = cv2.resize(image, None, fx=0.2, fy=0.2)

'''
    Crop The Image using canny edge detection and contour formations. Use BilateralFiltering to remove the desired noises.
'''
image_bounds = get_image_bounds(image, image.shape[0], image.shape[1])
bounded_image = image[image_bounds[0][0]: image_bounds[1][0], image_bounds[0][1]: image_bounds[1][1]]

'''
    Convert the image to a grayscale image with either 0 or 1 intensity.
'''
gray_image = cv2.cvtColor(bounded_image, cv2.COLOR_BGR2GRAY)
'''
    MAX Value = 255 (White)
    Min Value = 0 (Black)
'''
for w in range(gray_image.shape[1]):
    for h in range(gray_image.shape[0]):
        if gray_image[h][w] > THRESHOLD:
            gray_image[h][w] = MAX_VALUE
        else:
            gray_image[h][w] = MIN_VALUE

'''
    Converting to grayscale makes it easier to work/tweak around images and apply heuristics.
'''

# Get the lowest left point where the signature starts.
lowest_x = 0
lowest_y = 0

for w in range(gray_image.shape[1]):
    for h in range(gray_image.shape[0]):
        if gray_image[h][w] == 0:
            if lowest_x < h:
                lowest_x = h
                lowest_y = w


bounded_image[lowest_x, lowest_y:] = [0, 255, 0]

# get the right most lowest point.
# join them to get the slope of inclination.

lowest_rx = 0
lowest_ry = gray_image.shape[0]
for w in range(gray_image.shape[1]):
    for h in range(gray_image.shape[0]):
        if gray_image[h][w] == 0:
            if lowest_rx < w:
                lowest_rx = w
                lowest_ry = h

'''
    Join the end points to get the line. Calculate slope using this line equation.
'''
cv2.line(bounded_image, (lowest_y, lowest_x), (lowest_rx, lowest_ry), (0, 255, 0), 2)

cv2.imshow('Samarth Original Bounded Sign', bounded_image)
cv2.imwrite('./test/LineInclinationImage.png', bounded_image)
cv2.imwrite('./test/GrayScaleImage.png', gray_image)
cv2.imshow('Samarth Grayscale Sign', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
