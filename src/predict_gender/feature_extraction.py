import os

import pandas as pd

from constants.constants import MAX_LENGTH_DIRECTION_, NUMBER_PIXEL_DIRECTION_, test_source, input_source
from main import get_dataset_values

columns = ["Name", "Intensity_Threshold", "Ratio_Of_Black_Pixels",
           "External_Contours", "Internal_Contours", "Max_Min_Height_Ratio",
           "Max_Min_Width_Ratio", "Contour_Slope", "Slant_Angle"]

for i in range(1, 9):
    columns.append(MAX_LENGTH_DIRECTION_ + str(i))

for i in range(1, 4):
    for j in range(1, 9):
        columns.append(NUMBER_PIXEL_DIRECTION_ + str(i) + "_" + str(j))

df = pd.DataFrame(columns=columns)

for root, dirs, filename in os.walk(test_source):
    for f in filename:
        threshold, percentage_of_black_pixels, external_contours_number, internal_contours_number, \
        max_min_height_ratio, max_min_width_ratio, contour_mean_slope, max_length_dict, image_direction_pixel_feature, \
        slant_angle = get_dataset_values(f, test_source)
        data = []
        data.extend((f, threshold, percentage_of_black_pixels, external_contours_number, internal_contours_number,
                     max_min_height_ratio, max_min_width_ratio, contour_mean_slope, slant_angle))
        for i in range(1, 9):
            if max_length_dict.has_key(MAX_LENGTH_DIRECTION_ + str(i)):
                data.append(max_length_dict[MAX_LENGTH_DIRECTION_ + str(i)])
            else:
                data.append(0)
        for i in range(1, 4):
            for j in range(1, 9):
                if image_direction_pixel_feature.has_key(NUMBER_PIXEL_DIRECTION_ + str(i) + "_" + str(j)):
                    data.append(image_direction_pixel_feature[NUMBER_PIXEL_DIRECTION_ + str(i) + "_" + str(j)])
                else:
                    data.append(0)
        df.loc[len(df)] = data
        print df
        df.to_csv('../../Dataset/test.csv', sep='\t')
