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
    cv2.drawContours(contoured, contours, -1, (255, 0, 0), contour_thickness)
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

