import numpy as np
import cv2
# Returns the length of the hornet in terms of pixel count

def hornet_length(picture) -> int:
    
    scale = 100 # Number of pixels per millimeter
    
    # Pixel count
    pixel_count = 0
    
    array_image = np.asarray(picture)
    print(array_image.shape)
    
    
    
    length_value = np.divide(pixel_count, scale)
    
    return length_value