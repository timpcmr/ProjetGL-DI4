from .picture_metadata import picture_metadata
from .xmlwriter import xmlwriter

def xmlgenerator(caracteristics : dict, filename : str, trap_reference : str = '') -> int:
    
    """Fonction pilotant la génération du fichier XML de sortie
    
    Args:
        caracteristics (dict): Dictionnaire contenant les caractéristiques du frelon
        filename (str): Chemin d'accès à l'image
        trap_reference (str, optional): Référence du piège. La valeur par défaut est ''.

    Returns:
        int: Code de retour de la fonction
    """
    
    metadata = picture_metadata(filename)
    xmlwriter(caracteristics, metadata, filename, trap_reference)
    
    return 0