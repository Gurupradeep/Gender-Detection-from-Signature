import cv2


def find_largest_bounding_box_from_contours(contours):
    largest_bounding_x_start, largest_bounding_y_start = (100000, 100000)
    largest_bounding_x_end, largest_bounding_y_end = (0, 0)
    # assuming that major foreground is always bigger in size than any unwanted backgrounds considered as foreground.
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if x < largest_bounding_x_start:
            largest_bounding_x_start = x
        if y < largest_bounding_y_start:
            largest_bounding_y_start = y
        if x + w > largest_bounding_x_end:
            largest_bounding_x_end = x + w
        if y + h > largest_bounding_y_end:
            largest_bounding_y_end = y + h
    return largest_bounding_x_start, largest_bounding_x_end, largest_bounding_y_start, largest_bounding_y_end


def __get_contours(edged):
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def detect_edge(image, canny_th1=40, canny_th2=20, blurr_lens_size=50, blurr_sigma_1=300, blurr_sigma_2=300):
    image_blurred = cv2.bilateralFilter(image.copy(), blurr_lens_size, blurr_sigma_1, blurr_sigma_2)
    edged = cv2.Canny(image_blurred, canny_th1, canny_th2)
    return edged


def draw_contours(image_bgr, contour_thickness=7, canny_th1=40, canny_th2=20, blurr_lens_size=50, blurr_sigma_1=50,
                  blurr_sigma_2=50):
    edged = detect_edge(image_bgr, canny_th1, canny_th2, blurr_lens_size, blurr_sigma_1, blurr_sigma_2)
    contours = __get_contours(edged)
    contoured = edged.copy()
    cv2.drawContours(contoured, contours, -1, (0, 0, 0), contour_thickness)
    return contoured, contours


def get_image_bounds(image, h, w, contour_thickness=7, canny_th1=40, canny_th2=20, blurr_lens_size=50,
                     blurr_sigma_1=200,
                     blurr_sigma_2=200):
    contoured, contours = draw_contours(image_bgr=image, contour_thickness=contour_thickness, canny_th1=canny_th1,
                                        canny_th2=canny_th2, blurr_lens_size=blurr_lens_size,
                                        blurr_sigma_1=blurr_sigma_1,
                                        blurr_sigma_2=blurr_sigma_2)
    x_start, x_end, y_start, y_end = find_largest_bounding_box_from_contours(contours)
    bounds = [[y_start, x_start], [y_end, x_end]]
    return bounds


def invert_grayscale_image(image):
    for w in range(image.shape[1]):
        for h in range(image.shape[0]):
            image[h][w] = 0
    return image


def get_max_length_dir(image, direction, w, h):
    length = 0
    if direction == 1:
        while image[h, w] == 0:
            if w == image.shape[1]:
                break
            if image[h, w] == 0:
                w += 1
                length += 1
    elif direction == 2:
        while image[h, w] == 0:
            if h < 0 or w == image.shape[1]:
                break
            if image[h, w] == 0:
                length += 1
                w += 1
                h -= 1
    elif direction == 3:
        while image[h, w] == 0:
            if h < 0:
                break
            if image[h, w] == 0:
                length += 1
                h -= 1
    elif direction == 4:
        while image[h, w] == 0:
            if h < 0 or w < 0:
                break
            if image[h, w] == 0:
                length += 1
                w -= 1
                h -= 1
    elif direction == 5:
        while image[h, w] == 0:
            if w < 0:
                break
            if image[h, w] == 0:
                length += 1
                w -= 1
    elif direction == 6:
        while image[h, w] == 0:
            if w < 0 or h == image.shape[0]:
                break
            if image[h, w] == 0:
                length += 1
                w -= 1
                h += 1
    elif direction == 7:
        while image[h, w] == 0:
            if h == image.shape[0]:
                break
            if image[h, w] == 0:
                length += 1
                h += 1
    elif direction == 8:
        while image[h, w] == 0:
            if h == image.shape[0] or w == image.shape[1]:
                break
            if image[h, w] == 0:
                length += 1
                w += 1
                h += 1
    else:
        print "Wrong Direction Given As Input"
    return length


def get_direction_count(image, h, w, window_size, posH, posW):
    direction_count = dict()
    if posW+1 < w and image[posH][posW+1] == 0:
        if direction_count.has_key(1):
            direction_count[1] += 1
        else:
            direction_count[1] = 1
    else:
        direction_count[1] = 0

    if posW+1 < w and posH-1 >= 0 and image[posH-1][posW+1] == 0:
        if direction_count.has_key(2):
            direction_count[2] += 1
        else:
            direction_count[2] = 1
    else:
        direction_count[2] = 0

    if posH-1 >= 0 and image[posH-1][posW] == 0:
        if direction_count.has_key(3):
            direction_count[3] += 1
        else:
            direction_count[3] = 1
    else :
        direction_count[3] = 0

    if posW-1 >= 0 and posH-1 >= 0 and image[posH-1][posW-1] == 0:
        if direction_count.has_key(2):
            direction_count[4] += 1
        else:
            direction_count[4] = 1
    else:
        direction_count[4] = 0

    if posW-1 >= 0 and image[posH][posW-1] == 0:
        if direction_count.has_key(5):
            direction_count[5] += 1
        else:
            direction_count[5] = 1
    else:
        direction_count[5] = 0

    if posW-1 >= 0 and posH+1 < h and image[posH+1][posW-1] == 0:
        if direction_count.has_key(6):
            direction_count[6] += 1
        else:
            direction_count[6] = 1
    else :
        direction_count[6] = 0

    if posH+1 < w and image[posH+1][posW] == 0:
        if direction_count.has_key(7):
            direction_count[7] += 1
        else:
            direction_count[7] = 1
    else:
        direction_count[7] = 0

    if posW+1 < w and posH+1 < h and image[posH+1][posW+1] == 0:
        if direction_count.has_key(8):
            direction_count[8] += 1
        else:
            direction_count[8] = 1
    else:
        direction_count[8] = 0
