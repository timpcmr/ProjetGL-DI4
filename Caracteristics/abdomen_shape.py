import numpy as np
import cv2

def abdomen_shape(picture_array : np.ndarray, sting_coordinates : tuple) -> str:
    
    """Détermine la forme de l'abdomen du frelon
    
    Args:
        picture_array (np.ndarray): Matrice de l'image bianire du frelon
        sting_coordinates (tuple): Coordonnées du dard/extremité de l'abdomen
    
    Returns:
        str: Forme de l'abdomen
    
    """
    
    
    return