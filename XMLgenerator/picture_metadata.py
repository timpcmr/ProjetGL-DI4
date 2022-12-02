import csv
from pathlib import Path
def picture_metadata(filename : str) -> dict:
    """Lis les métadonnées d'une phtographie stockée dans son fichier descriptif .csv et les renvoie sous forme de dictionnaire.

    Args:
        filename (str): Chemin d'accès au .csv

    Returns:
        dict: Dictioanire contenant les métadonnées de l'image
    """
    
    print(filename)
    
    # Initialisation of the dictionary
    metadata = dict()
    
    # Getting the metadata file
    csv_path = Path(filename).stem + '.csv'
    csv_path = Path('Footage') / csv_path
    print(csv_path)
    with open(csv_path, 'r') as file:
        csvreader = csv.reader(file, delimiter = ';')
        rows_list = list(csvreader)
        
        for i in range(len(rows_list[0])):
            metadata[rows_list[0][i]] = rows_list[1][i]
    
    return metadata