import cv2
import matplotlib.pyplot as plt
from common.image_helper import get_image_bounds, invert_grayscale_image, get_max_length_dir, get_direction_count
from constants.constants import THRESHOLD, MAX_VALUE, MIN_VALUE, MAX_LENGTH_DIRECTION_, NUMBER_PIXEL_DIRECTION_, \
    SLOPE_ANGLE, input_source, WIDTH, HEIGHT
from helper.helper import get_external_and_internal_contours, get_slope_height_ratio, get_max_length_direction, \
    image_direction_pixels


def get_dataset_values(image_path, path):
    image = cv2.imread(path + image_path)
    width = image.shape[1]
    height = image.shape[0]
    image = cv2.resize(image, None, fx=WIDTH*1.0/width, fy=HEIGHT*1.0/height)
    '''
        Crop The Image using canny edge detection and contour formations. Use BilateralFiltering to remove the desired noises.
    '''
    image_bounds = get_image_bounds(image, image.shape[0], image.shape[1])
    bounded_image = image[max(0, image_bounds[0][0] - 8): min(image.shape[0], image_bounds[1][0] + 8),
                    max(image_bounds[0][1] - 8, 0): min(image.shape[1], image_bounds[1][1] + 8)]

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
    number_of_pixels_to_be_considered = 0
    for x_value in x_values_all:
        if x_value <= THRESHOLD:
            x_values.append(x_value)
            y_values.append(x[x_value])
            number_of_pixels_to_be_considered += x[x_value]

    threshold = THRESHOLD
    number_of_pixels_till_threshold = 0
    for x_value in x_values:
        if number_of_pixels_till_threshold >= 0.75*number_of_pixels_to_be_considered:
            threshold = x_value - 1
            break
        number_of_pixels_till_threshold += x[x_value]

    '''
        Draw histogram of the intensity vs count of pixels.
    '''
    # todo: Calculating threshold value depending on the values of the intensity.
    '''
    plt.plot(x_values, y_values)
    plt.savefig('intensity_count.pdf')
    plt.show()
    '''
    '''
        MAX Value = 255 (White)
        Min Value = 0 (Black)
    '''

    # todo: Change the value of Threshold as calculated above.

    number_of_black_pixel = 0
    for w in range(gray_image.shape[1]):
        for h in range(gray_image.shape[0]):
            if gray_image[h][w] > threshold:
                gray_image[h][w] = MAX_VALUE
            else:
                gray_image[h][w] = MIN_VALUE
                number_of_black_pixel += 1

    print "Number of Black Pixels after Gray-Scale threshold: " + str(number_of_black_pixel)

    percentage_of_black_pixels = number_of_black_pixel * 1.0 / (gray_image.shape[0] * gray_image.shape[1])

    contours, hierarchy = cv2.findContours(gray_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    external_contours_number, internal_contours_number = get_external_and_internal_contours(gray_image=gray_image)
    print "Number of External Contours : %d, Internal Contours : %d" % (
        external_contours_number, internal_contours_number)
    contour_heights, contour_widths = get_slope_height_ratio(contours, hierarchy)
    for i in range(len(contour_widths)):
        if contour_widths[i] == 0:
            contour_widths[i] = 1

    for i in range(len(contour_heights)):
        if contour_heights[i] == 0:
            contour_heights[i] = 1

    print "heights : ", contour_heights
    print "widths : ", contour_widths

    max_min_height_ratio = 0.0
    max_min_width_ratio = 0.0
    if len(contour_heights) > 0:
        max_height = max(contour_heights)
        min_height = max(min(contour_heights), 1)
        max_min_height_ratio = max_height * 1.0 / min_height

    if len(contour_widths) > 0:
        max_width = max(contour_widths)
        min_width = max(min(contour_widths), 1)
        max_min_width_ratio = max_width * 1.0 / min_width
    # FEATURE :

    contours_slopes = []

    for i in range(len(contour_widths)):
        contours_slopes.append(contour_heights[i] * 1.0 / contour_widths[i])

    # FEATURE:
    print "slopes : ", contours_slopes

    contour_mean_slope = sum(contours_slopes)*1.0/len(contours_slopes)

    max_length_each_direction = get_max_length_direction(gray_image=gray_image)
    max_length = max(max_length_each_direction.values())
    max_length_dict = dict()
    # FEATURE :
    for key in max_length_each_direction.keys():
        max_length_dict[MAX_LENGTH_DIRECTION_ + str(key)] = max_length_each_direction[key] * 1.0 / max_length

    # FEATURES :
    image_direction_pixel_feature = dict()
    image_direction_dict = image_direction_pixels(gray_image)
    for key in image_direction_dict.keys():
        FEATURE_NAME = NUMBER_PIXEL_DIRECTION_ + str(key)
        wndw_length_sum = sum(image_direction_dict[key].values())
        for key1 in image_direction_dict[key]:
            FEATURE_NAME_APPENDED = FEATURE_NAME + "_" + str(key1)
            image_direction_pixel_feature[FEATURE_NAME_APPENDED] = image_direction_dict[key][
                                                                       key1] * 1.0 / wndw_length_sum

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
    cv2.line(bounded_image, (lowest_y, lowest_x), (lowest_rx, lowest_ry), (0, 255, 0), 2)

    # Feature
    slant_angle = (lowest_rx - lowest_y) * 1.0 / (lowest_ry - lowest_x)

    '''
    cv2.imshow('Samarth Original Bounded Sign', bounded_image)
    cv2.imwrite('./test/LineInclinationImage.png', bounded_image)
    cv2.imwrite('./test/GrayScaleImage.png', gray_image)
    cv2.imshow('Samarth Grayscale Sign', gray_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return threshold, percentage_of_black_pixels, external_contours_number, internal_contours_number, \
           max_min_height_ratio, max_min_width_ratio, contour_mean_slope, max_length_dict, image_direction_pixel_feature, \
           slant_angle
