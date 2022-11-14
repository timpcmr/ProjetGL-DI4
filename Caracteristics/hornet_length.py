import numpy as np
import cv2
# Returns the length of the hornet in terms of pixel count

def non_zero_pixels(line : np.ndarray) -> int:
    
    return np.divide(np.count_nonzero(line),4)

def bounding_lines(array_image : np.ndarray):
    
    number_of_lines = array_image.shape[0]
    number_of_columns = array_image.shape[1]
    
    print("Number of lines:", number_of_lines)
    
    # Finding the lower horizontal line to frame the hornet
    counter = number_of_lines
    pixel_count = 0
    
    while pixel_count < 400 and counter > 0:
        pixel_count = non_zero_pixels(array_image[counter - 1])
        counter -= 1
    
    lower_line = counter
    
    # Finding the upper horizontal line to frame the hornet
    
    counter = 0
    pixel_count = 0
    
    while pixel_count < 400 and counter < number_of_lines:
        pixel_count = non_zero_pixels(array_image[counter])
        counter += 1
    
    upper_line = counter
    
    # Finding the left vertical line to frame the hornet
    
    counter = 0
    pixel_count = 0
    
    while pixel_count < 100 and counter < number_of_columns:
        pixel_count = non_zero_pixels(array_image[:, counter])
        counter += 1
    
    left_line = counter
    
    print("Upper line:", upper_line)
    print("Lower line:", lower_line)
    print("Left line:", left_line)
    
    return upper_line, lower_line, left_line
    

def hornet_length(picture) -> int:
    
    scale = 100 # Number of pixels per millimeter
    
    array_image = np.asarray(picture)
    number_of_lines = array_image.shape[0]
    number_of_columns = array_image.shape[1]
    
    
    upper_line, lower_line, left_line = bounding_lines(array_image)

    """"
    # Drawing the lines on the image
    
    # Lower line
    cv2.line(picture, (0, lower_line), (number_of_columns, lower_line), (0, 0, 255), 2)
    
    # Upper line
    cv2.line(picture, (0, upper_line), (number_of_columns, upper_line), (0, 0, 255), 2)
    
    # Left line
    cv2.line(picture, (left_line, 0), (left_line, number_of_lines), (0, 0, 255), 2)
    
    cv2.imshow("Hornet length", picture)
    cv2.waitKey(0)
    """
    
    extracted_array = array_image[upper_line:lower_line, left_line:number_of_columns]
    
    pixel_count_list = list()
    for line in extracted_array:
        pixel_count_list.append(non_zero_pixels(line))
    
    pixel_count = np.ceil(np.max(pixel_count_list))
    
    print("Pixel count:", pixel_count)
    
    length_value = np.divide(pixel_count, scale)
    
    return length_value