import numpy as np
import cv2
import matplotlib.pyplot as plt

# Should be launch with the terminal by putting the image to analyse in first parameter
def cutout(filename : str) -> np.ndarray:
    # Loading images
    img = cv2.imread(filename)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    if img is None:
        raise FileNotFoundError
    
    img_GREY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    light_yellow_BGR, dark_yellow_BGR = (100, 240, 250), (60, 170, 180) #RGB values for yellow
    # Creating the main mask
    
    mask = cv2.threshold(img_GREY, 90, 255, cv2.THRESH_BINARY)
    
    # Creating a mask for the yellow color in the image
    
    temp_mask2 = cv2.inRange(img, dark_yellow_BGR, light_yellow_BGR)
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
