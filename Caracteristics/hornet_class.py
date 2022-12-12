from .abdomen_shape import *
from .hornet_length import *
from xml.dom import minidom
from datetime import datetime
import os

def hornet_class(hornet_binary_mask : np.ndarray, picturefile : str) -> dict:
    
    """Fonction pilotant la classification du frelon

    Args:
        hornet_binary_mask (np.ndarray): Matrice de l'image binaire du frelon
        picturefile (str): Chemin d'accès à l'image

    Returns:
        dict: Caste du frelon
    """

    #Ouverture du xml des paramètres
    parameters = minidom.parse('parameters.xml')

    #Récupération des paramètres
    seuil = int(parameters.getElementsByTagName('seuil')[0].firstChild.data)
    actual_month = int(datetime.now().month)
    scale = int(parameters.getElementsByTagName('echelle')[0].firstChild.data)
    flag = int(parameters.getElementsByTagName('forcer_debut_saison')[0].firstChild.data)
    print("mois actuel :", actual_month, "| seuil :", seuil, "| échelle :", scale, "| forcer début saison :", flag)

    # Initialisation du dictionnaire de retour
    caracteristics = dict()
    
    # Recherche de la longueur du frelon
    hornet_length_value, sting_coordinates = hornet_length(hornet_binary_mask, picturefile)
    reel_length = np.divide(hornet_length_value, scale)
    caracteristics['hornetlength'] = str(reel_length)

    # Recherche de la forme de l'abdomen
    abdomen_shape_value = abdomen_shape(hornet_binary_mask, sting_coordinates)
    caracteristics['abdomenshape'] = abdomen_shape_value
    
    #Détermination de la caste
    caste = ""
    if actual_month <= seuil and flag == 0:
        caracteristics['cast'] = "Fondatrice"
        year = datetime.now().year
        path = "Results\length" + str(year) + ".xml"
        if not os.path.exists(path):
            root = minidom.Document()
            data = root.createElement('data')
            root.appendChild(data)
            root.writexml(open('Results\length'+str(year)+".xml", 'w'), indent="  ", addindent="  ", newl='\n')
            root.unlink()
        root = minidom.parse(path)
        data = root.getElementsByTagName('data')[0]
        picture = root.createElement('picture')
        picture.setAttribute('name', picturefile)
        data.appendChild(picture)
        length = root.createElement('length')
        length.setAttribute('unit', 'mm')
        length.appendChild(root.createTextNode(str(reel_length)))
        picture.appendChild(length)
        root.writexml(open('Results\length'+str(year)+".xml", 'w'), indent="  ", addindent="  ", newl='\n')
        root.unlink()
    else:
        if abdomen_shape_value == "pointu" and reel_length > 10:
            caste = "Fondatrice"
        elif abdomen_shape_value == "pointu" and reel_length <= 10:
            caste = "Ouvriere"
        elif abdomen_shape_value == "rond":
            caste = "Male"
        if caste != "":
            caracteristics['cast'] = caste
    return caracteristics