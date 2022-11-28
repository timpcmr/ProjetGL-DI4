import numpy as np
import cv2

def cutout(filename : str) -> np.ndarray:
    """Fonction effectuant le découpage de l'image

    Args:
        filename (str): Chemin d'accès à l'image

    Raises:
        FileNotFoundError: Si l'image n'a pas pu être lue

    Returns:
        np.ndarray: Matrice du découpage de l'image
    """
    
    # Loading images
    img = cv2.imread(filename)
    
    if img is None:
        raise FileNotFoundError
    
    img_GREY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    color1 = (10, 200, 20)  #Darker Yellow to keep
    color2 = (45, 255, 255)  #Lighter Yellow to keep

    # Creating the main mask
    
    mask = cv2.threshold(img_GREY, 90, 255, cv2.THRESH_BINARY)
    
    # Creating a mask for the yellow color in the image
    temp_mask2 = cv2.inRange(img_HSV, color1, color2)
    mask2 = cv2.bitwise_not(temp_mask2)
    
    # Combining the two masks
    
    combined_mask = cv2.bitwise_and(mask[1], mask2)
    
    # Getting rid of artifacts
    intermediate_smoothed_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    smoothed_mask = cv2.morphologyEx(intermediate_smoothed_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4)))
    
    cv2.imshow("Mask", smoothed_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    cv2.imwrite("Footage/17_cutout.jpg", smoothed_mask)
    
    return smoothed_mask
