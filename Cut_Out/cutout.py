import numpy as np
import cv2
import matplotlib.pyplot as plt

# Should be launch with the terminal by putting the image to analyse in first parameter
def bgr_to_hsv(rgb : tuple) -> tuple:
 
    # R, G, B values are divided by 255
    # to change the range from 0..255 to 0..1:
    b, g, r = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
 
    # h, s, v = hue, saturation, value
    cmax = max(r, g, b)    # maximum of r, g, b
    cmin = min(r, g, b)    # minimum of r, g, b
    diff = cmax-cmin       # diff of cmax and cmin.
 
    # if cmax and cmax are equal then h = 0
    if cmax == cmin:
        h = 0
     
    # if cmax equal r then compute h
    elif cmax == r:
        h = (60 * ((g - b) / diff) + 360) % 360
 
    # if cmax equal g then compute h
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
 
    # if cmax equal b then compute h
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360
 
    # if cmax equal zero
    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100
 
    # compute v
    v = cmax * 100
    return h, s, v

def cutout(filename : str) -> np.ndarray:
    # Loading images
    img = cv2.imread(filename)
    
    if img is None:
        raise FileNotFoundError
    
    img_GREY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    light_yellow_BGR, dark_yellow_BGR = (130, 240, 250), (50, 170, 180) #RGB values for yellow
    light_yellow_HSV, dark_yellow_HSV = bgr_to_hsv(light_yellow_BGR), bgr_to_hsv(dark_yellow_BGR) #HSV values for yellow
    
    print (light_yellow_HSV, dark_yellow_HSV)
    
    # Creating the main mask
    
    mask = cv2.threshold(img_GREY, 90, 255, cv2.THRESH_BINARY)
    
    # Creating a mask for the yellow color in the image
    
    temp_mask2 = cv2.inRange(img_HSV, dark_yellow_HSV, light_yellow_HSV)
    mask2 = cv2.bitwise_not(temp_mask2)
    
    # Combining the two masks
    
    combined_mask = cv2.bitwise_and(mask[1], mask2)
    
    print(combined_mask.shape)
    print(cv2.countNonZero(combined_mask))
    cv2.imshow("Mask", combined_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    cv2.imwrite("Footage/17_cutout.jpg", mask[1])
    
    return mask[1]
