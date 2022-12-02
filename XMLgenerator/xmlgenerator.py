from .picture_metadata import picture_metadata
from .xmlwriter import xmlwriter

def xmlgenerator(caracteristics : dict, filename : str) -> int:
    
    """Fonction pilotant la génération du fichier XML de sortie
    
    Args:
        caracteristics (dict): Dictionnaire contenant les caractéristiques du frelon
        filename (str): Chemin d'accès à l'image

    Returns:
        int: Code de retour de la fonction
    """
    
    # Getting the picture metadata
    metadata = picture_metadata(filename)
    
    # Writing the XML file
    xmlwriter(caracteristics, metadata, filename)
    
    return 0