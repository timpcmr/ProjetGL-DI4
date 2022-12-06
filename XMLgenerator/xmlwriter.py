from xml.dom import minidom
from pathlib import Path
import os

def xmlwriter(caracteristics : dict, picture_metadata : dict, filename : str) -> int:
    
    """Fonction d'écriture du fichier XML de sortie
    
    Args:
        caracteristics (dict): Dictionnaire contenant les caractéristiques du frelon
        picture_metadata (dict): Dictionnaire contenant les métadonnées de l'image
        filename (str): Chemin d'accès à l'image
        trap_reference (str): Référence du piège

    Returns:
        int: Code de retour de la fonction
    """
    
    # Génératon du nom du fichier XML de sortie
    
    outputname = Path(filename.removeprefix("Footage/")).stem + '.xml'
    
    # Formatage, remplissage et écriture du fichier XML
    
    root = minidom.Document()
    
    # Label principal
    data = root.createElement('data')
    root.appendChild(data)
    
    # Label pour chaque image
    picture = root.createElement('picture')
    picture.setAttribute('name', filename.removeprefix("Footage/"))
    data.appendChild(picture)
    
    # Labels pour les caractéristiques
    caracteristics_label = root.createElement('caracteristics')
    picture.appendChild(caracteristics_label)
    
    cast = root.createElement('cast') # Si déterminé
    cast.appendChild(root.createTextNode(caracteristics.get('cast', 'UNDEFINED')))
    caracteristics_label.appendChild(cast)
    
    hornetlength = root.createElement('hornetlength')
    hornetlength.setAttribute('unit', 'mm')
    hornetlength.appendChild(root.createTextNode(caracteristics.get('hornetlength', 'UNDEFINED')))
    caracteristics_label.appendChild(hornetlength)
    
    abdomenshape = root.createElement('abdomenshape')
    abdomenshape.appendChild(root.createTextNode(caracteristics.get('abdomenshape', 'UNDEFINED')))
    caracteristics_label.appendChild(abdomenshape)
    
    wingsspacing = root.createElement('wingsspacing') # Si déterminé
    wingsspacing.setAttribute('unit', 'mm')
    wingsspacing.appendChild(root.createTextNode(caracteristics.get('wingsspacing', 'UNDEFINED')))
    caracteristics_label.appendChild(wingsspacing)
    
    # Labels pour les métadonnées
    metadata = root.createElement('metadata')
    picture.appendChild(metadata)
    
    date = root.createElement('date')
    date.appendChild(root.createTextNode(picture_metadata.get('Date', 'UNDEFINED')))
    metadata.appendChild(date)
    
    time = root.createElement('time')
    time.appendChild(root.createTextNode(picture_metadata.get('Heure', 'UNDEFINED')))
    metadata.appendChild(time)
    
    trapreference = root.createElement('trapreference') 
    trapreference.appendChild(root.createTextNode(picture_metadata.get('Reference', 'UNDEFINED')))
    metadata.appendChild(trapreference)
    
    trapreference = root.createElement('trapcode') 
    trapreference.appendChild(root.createTextNode(picture_metadata.get('Code', 'UNDEFINED')))
    metadata.appendChild(trapreference)
    
    
    # Crée le fichier XML et l'enregistre (si le dossier n'existe pas, il est créé)
    if not os.path.exists('Results'):
        os.makedirs('Results')
    
    root.writexml( open('Results/' + outputname, 'w'), indent="  ", addindent="  ", newl='\n')
    root.unlink()
    
    return 0