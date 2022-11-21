import numpy as np
import cv2

# Should be launch with the terminal by putting the image to analyse in first parameter
def cutout(filename : str) -> np.ndarray:
    # Loading images
    img = cv2.imread(filename)
    
    if img is None:
        raise FileNotFoundError
    
    img_GREY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    mask = cv2.threshold(img_GREY, 90, 255, cv2.THRESH_BINARY)
    
    cv2.imwrite("Footage/17_cutout.jpg", mask[1])
    
    return mask[1]
