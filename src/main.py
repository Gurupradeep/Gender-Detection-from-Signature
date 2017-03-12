import cv2
import matplotlib.pyplot as plt
from common.image_helper import get_image_bounds, invert_grayscale_image

THRESHOLD = 230
MAX_VALUE = 255
MIN_VALUE = 0

image = cv2.imread('./test/samarth.jpg')

image = cv2.resize(image, None, fx=0.2, fy=0.2)

'''
    Crop The Image using canny edge detection and contour formations. Use BilateralFiltering to remove the desired noises.
'''
image_bounds = get_image_bounds(image, image.shape[0], image.shape[1])
bounded_image = image[max(0, image_bounds[0][0] - 2): min(image.shape[1], image_bounds[1][0]+2) , max(image_bounds[0][1]-2, 0): min(image.shape[0], image_bounds[1][1]+2)]

'''
    Convert the image to a grayscale image with either 0 or 1 intensity.
'''
gray_image = cv2.cvtColor(bounded_image, cv2.COLOR_BGR2GRAY)
x = dict()
for w in range(gray_image.shape[1]):
    for h in range(gray_image.shape[0]):
        if x.has_key(gray_image[h][w]):
            x[gray_image[h][w]] += 1
        else:
            x[gray_image[h][w]] = 1

x_values_all = x.keys()
x_values = []
y_values = []
for x_value in x_values_all:
    if x_value <= 220:
        x_values.append(x_value)
        y_values.append(x[x_value])

'''
    Draw histogram of the intensity vs count of pixels.
'''

# todo: Calculating threshold value depending on the values of the intensity.

plt.plot(x_values, y_values)
plt.savefig('intensity_count.pdf')
plt.show()
'''
    MAX Value = 255 (White)
    Min Value = 0 (Black)
'''

# todo: Change the value of Threshold as calculated above.

number_of_black_pixel = 0
for w in range(gray_image.shape[1]):
    for h in range(gray_image.shape[0]):
        if gray_image[h][w] > THRESHOLD:
            gray_image[h][w] = MAX_VALUE
        else:
            gray_image[h][w] = MIN_VALUE
            number_of_black_pixel += 1

print "Number of Black Pixels after Gray-Scale threshold: " + str(number_of_black_pixel)


'''
    Measure of Writing movement.
'''
contours, hierarchy = cv2.findContours(gray_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


external_contours = []
internal_contours = []
# Imp: Count external and internal contours.
for hierarchy_info in hierarchy[0]:
    parent = hierarchy_info[3]
    if parent == -1:
        continue
    elif parent == 0:
        external_contours.append(parent)
    else:
        internal_contours.append(parent)

print "Number of External Contours : %d, Internal Contours : %d" %(len(external_contours), len(internal_contours))

bounded_image1 = bounded_image.copy()
gray_image1 = invert_grayscale_image(gray_image.copy())
cv2.drawContours(gray_image1, contours, -1, (0, 0, 0), 1)
cv2.imshow('Contours', gray_image1)

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
