from .abdomen_shape import *
from .hornet_length import *


def hornet_class(hornet_binary_mask : np.ndarray, picturefile : str) -> dict:
    
    """Fonction pilotant la classification du frelon

    Args:
        hornet_binary_mask (np.ndarray): Matrice de l'image binaire du frelon
        picturefile (str): Chemin d'accès à l'image

    Returns:
        dict: Caste du frelon
    """
    
    # Initialisation du dictionnaire de retour
    caracteristics = dict()
    
    # Recherche de la longueur du frelon
    hornet_length_value, sting_coordinates = hornet_length(hornet_binary_mask, picturefile)
    scale = 100
    reel_length = np.divide(hornet_length_value, scale)
    caracteristics["hornetlength"] = reel_length
    
    # Recherche de la forme de l'abdomen
    abdomen_shape_value = abdomen_shape(hornet_binary_mask, sting_coordinates)
    caracteristics["abdomenshape"] = abdomen_shape_value
    
    
    
    return caracteristics