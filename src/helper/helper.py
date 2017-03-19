import cv2

from common.image_helper import invert_grayscale_image, get_max_length_dir, get_direction_count
from constants.constants import Directions


def get_external_and_internal_contours(gray_image):
    contours, hierarchy = cv2.findContours(gray_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    gray_image1 = invert_grayscale_image(gray_image.copy())
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
    return len(external_contours), len(internal_contours)


def get_slope_height_ratio(contours, hierarchy):
    contour_heights = []
    contour_widths = []
    for contour_index in range(len(contours)):
        if hierarchy[0][contour_index][3] == -1:
            continue
        else:
            if len(contours[contour_index]) > 1:
                min_height = 100000
                max_height = 0
                min_width = 100000
                max_width = 0
                for ctrs in contours[contour_index]:
                    ctrs_values = ctrs[0]
                    min_height = min(min_height, ctrs_values[0])
                    max_height = max(max_height, ctrs_values[0])
                    min_width = min(min_width, ctrs_values[1])
                    max_width = max(max_width, ctrs_values[1])
                contour_heights.append(max_height - min_height)
                contour_widths.append(max_width - min_width)
    return contour_heights, contour_widths


def get_max_length_direction(gray_image):
    max_length_each_direction = dict()
    for h in range(gray_image.shape[0]):
        for w in range(gray_image.shape[1]):
            if gray_image[h][w] == 0:
                for direction in Directions:
                    length = get_max_length_dir(gray_image.copy(), direction, w, h)
                    if max_length_each_direction.has_key(direction):
                        max_length_each_direction[direction] = max(max_length_each_direction[direction], length)
                    else:
                        max_length_each_direction[direction] = length
    return max_length_each_direction


def image_direction_pixels(gray_image):
    image_direction_dict = dict()
    window_size = [1, 2, 3]
    for wnd_size in window_size:
        for w in range(gray_image.shape[1]):
            for h in range(gray_image.shape[0]):
                if gray_image[h][w] == 0:
                    direction_count = get_direction_count(gray_image.copy(), gray_image.shape[0], gray_image.shape[1],
                                                          wnd_size, h, w)
                    for key in direction_count.keys():
                        if image_direction_dict.has_key(wnd_size):
                            if image_direction_dict[wnd_size].has_key(key):
                                image_direction_dict[wnd_size][key] += direction_count[key]
                            else:
                                image_direction_dict[wnd_size][key] = direction_count[key]
                        else:
                            image_direction_dict[wnd_size] = dict()
    return image_direction_dict
