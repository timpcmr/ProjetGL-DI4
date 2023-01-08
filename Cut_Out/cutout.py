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
    
    # Charge l'image
    img = cv2.imread(filename)
    
    # Levée d'exception si l'image n'a pas pu être lue
    if img is None:
        raise FileNotFoundError
    
    img_GREY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    color1 = (10, 200, 20)  # Borne sombre du spectre de couleur jaune à garder
    color2 = (45, 255, 255)  # Borne claire du spectre de couleur jaune à garder

    # Création du masque principal (Masque de niveau de gris)
    
    mask = cv2.threshold(img_GREY, 90, 255, cv2.THRESH_BINARY)
    
    # Création du masque secondaire (Masque de couleur jaune)
    temp_mask2 = cv2.inRange(img_HSV, color1, color2)
    mask2 = cv2.bitwise_not(temp_mask2)
    
    # Addition des deux masques
    
    combined_mask = cv2.bitwise_and(mask[1], mask2)
    
    # Dilatation/érosion du masque pour supprimer les petits artefacts
    intermediate_smoothed_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    smoothed_mask = cv2.morphologyEx(intermediate_smoothed_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4)))
    
    return smoothed_mask
