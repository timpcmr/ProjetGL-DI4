import numpy as np
import cv2
# Returns the length of the hornet in terms of pixel count

def result_plot(picture, lower_line, upper_line, left_line, index_max, pixel_count, number_of_lines, number_of_columns, picturefile : str):
     # Drawing the lines on the image
    
    picture = cv2.cvtColor(picture, cv2.COLOR_GRAY2BGR)
    
    # Lower line
    cv2.line(picture, (0, lower_line), (number_of_columns, lower_line), (0, 0, 255), 2)
    
    # Upper line
    cv2.line(picture, (0, upper_line), (number_of_columns, upper_line), (0, 0, 255), 2)
    
    # Left line
    cv2.line(picture, (left_line, 0), (left_line, number_of_lines), (0, 0, 255), 2)
    
    # Right line
    
    positionning = int(left_line + pixel_count)
    cv2.line(picture, (positionning, 0), (positionning, number_of_lines), (0, 0, 255), 2)
    
    # Longest line
    cv2.line(picture, (left_line, index_max + upper_line), (positionning, index_max + upper_line), (0, 255, 0), 2)
    
    # Sting
    cv2.circle(picture, (positionning, index_max + upper_line), 10, (255, 75, 0), -1)
    
    cv2.imshow("Hornet length", picture)
    outputfile = picturefile[:-4] + "_length.jpg"
    outputfile = outputfile.removeprefix('Footage/')
    outputfile = "Footage/LengthPlots/" + outputfile
    print(outputfile)
    cv2.imwrite(outputfile, picture)
    cv2.waitKey(0)


def zero_pixels(line : np.ndarray) -> int:
    return line.shape[0] - np.count_nonzero(line)




def bounding_lines(array_image : np.ndarray):
    
    number_of_lines = array_image.shape[0]
    number_of_columns = array_image.shape[1]
    
    print("Number of lines:", number_of_lines)
    
    # Finding the lower horizontal line to frame the hornet
    counter = number_of_lines
    pixel_count = 0
    
    while pixel_count < 400 and counter > 0:
        pixel_count = zero_pixels(array_image[counter - 1])
        counter -= 1
    
    lower_line = counter
    
    # Finding the upper horizontal line to frame the hornet
    
    counter = 0
    pixel_count = 0
    
    while pixel_count < 400 and counter < number_of_lines:
        pixel_count = zero_pixels(array_image[counter])
        counter += 1
    
    upper_line = counter
    
    # Finding the left vertical line to frame the hornet
    
    counter = 0
    pixel_count = 0
    
    while pixel_count < 100 and counter < number_of_columns:
        pixel_count = zero_pixels(array_image[:, counter])
        counter += 1
    
    left_line = counter
    
    print("Upper line:", upper_line)
    print("Lower line:", lower_line)
    print("Left line:", left_line)
    
    return upper_line, lower_line, left_line

def hornet_length(picture, picturefile):
    
    scale = 100 # Number of pixels per millimeter
    
    array_image = np.asarray(picture)
    number_of_lines = array_image.shape[0]
    number_of_columns = array_image.shape[1]
    
    
    upper_line, lower_line, left_line = bounding_lines(array_image)
    
    extracted_array = array_image[upper_line:lower_line, left_line:number_of_columns]
    
    pixel_count_list = list()
    
    for line in extracted_array:
        #pixel_count_list.append(non_zero_pixels(line))
        pixel_count_list.append(zero_pixels(line))
    
    pixel_count = np.max(pixel_count_list)
    index_max = pixel_count_list.index(pixel_count)
    
    #result_plot(picture, lower_line, upper_line, left_line, index_max, pixel_count, number_of_lines, number_of_columns, picturefile)
    
    print("Pixel count:", pixel_count)
    
    length_value = np.divide(pixel_count, scale)
    
    print("Length value:", length_value, "mm")
    
    index_max_global = index_max + upper_line
    
    return length_value, index_max_global