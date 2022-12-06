import numpy as np
import cv2

# Retourne la longueur du corps du frelon

def result_plot(picture : np.ndarray, lower_line : int, upper_line : int, left_line : int, index_max : int, pixel_count : int, number_of_lines : int, number_of_columns : int, picturefile : str) -> tuple:
    
    """Fonction d'affichage des lignes de recherche du dard
    
    Args:
        picture (np.ndarray): Matrice de l'image binaire du frelon
        lower_line (int): Ligne inférieure de la zone d'analyse
        upper_line (int): Ligne supérieure de la zone d'analyse
        left_line (int): Colonne gauche de la zone d'analyse
        index_max (int): Indice de la ligne de la zone d'analyse contenant le plus de pixels noirs
        pixel_count (int): Nombre de pixels noirs de la ligne de la zone d'analyse contenant le plus de pixels noirs
        number_of_lines (int): Nombre de lignes de la matrice de l'image binaire du frelon
        picturefile (str): Chemin d'accès à l'image

    Returns:
        int: Code de retour de la fonction
    """
    
    # Dessin des lignes de recherche
    
    picture = cv2.cvtColor(picture, cv2.COLOR_GRAY2BGR)
    
    # Ligne inférieure
    cv2.line(picture, (0, lower_line), (number_of_columns, lower_line), (0, 0, 255), 2)
    
    # Ligne supérieure
    cv2.line(picture, (0, upper_line), (number_of_columns, upper_line), (0, 0, 255), 2)
    
    # Ligne gauche
    cv2.line(picture, (left_line, 0), (left_line, number_of_lines), (0, 0, 255), 2)
    
    # Ligne droite
    
    positionning = int(left_line + pixel_count)
    cv2.line(picture, (positionning, 0), (positionning, number_of_lines), (0, 0, 255), 2)
    
    # Ligne de longueur maximale
    cv2.line(picture, (left_line, index_max + upper_line), (positionning, index_max + upper_line), (0, 255, 0), 2)
    
    # Extéminté de la ligne de longueur maximale
    cv2.circle(picture, (positionning, index_max + upper_line), 10, (255, 75, 0), -1)
    
    cv2.imshow("Hornet length", picture)
    
    # Ecriture de l'image avec les lignes de recherche dessinées pour démonstration
    outputfile = picturefile[:-4] + "_length.jpg"
    outputfile = outputfile.removeprefix('Footage/')
    outputfile = "Footage/LengthPlots/" + outputfile
    print(outputfile)
    cv2.imwrite(outputfile, picture)
    cv2.waitKey(0)
    return 0


def zero_pixels(line : np.ndarray) -> int:
    
    """Fonction de comptage des pixels noirs d'une ligne
    
    Args:
        line (np.ndarray): Ligne de pixels à traiter
    
    Returns:
        int: Nombre de pixels noirs de la ligne
    """
    
    return line.shape[0] - np.count_nonzero(line)

def bounding_lines(array_image : np.ndarray) -> tuple:
    
    """Détermine les lignes/colonnes délimitant de la zone d'analyse du frelon
    
    Args:
        array_image (np.ndarray): Matrice de l'image binaire du frelon

    Returns:
        tuple: Indices des lignes/colonnes délimitant de la zone d'analyse du frelon
    """
    
    # Récupération du nombre de lignes et de colonnes de la matrice de l'image binaire du frelon
    number_of_lines = array_image.shape[0]
    number_of_columns = array_image.shape[1]
    
    print("Number of lines:", number_of_lines)
    
    # Recherche le la ligne inférieure de la zone d'analyse
    counter = number_of_lines
    pixel_count = 0
    
    horizontal_number = array_image.shape[1] * 0.4
    while pixel_count < horizontal_number and counter > 0:
        pixel_count = zero_pixels(array_image[counter - 1])
        counter -= 1
    
    lower_line = counter
    
    # Recherche le la ligne supérieure de la zone d'analyse
    
    counter = 0
    pixel_count = 0
    
    while pixel_count < horizontal_number and counter < number_of_lines:
        pixel_count = zero_pixels(array_image[counter])
        counter += 1
    
    upper_line = counter
    
    # Recherche de la colonne gauche de la zone d'analyse
    
    counter = 0
    pixel_count = 0
    
    vertical_number = array_image.shape[0] * 0.1
    while pixel_count < vertical_number and counter < number_of_columns:
        pixel_count = zero_pixels(array_image[:, counter])
        counter += 1
    
    left_line = counter
    
    print("Upper line:", upper_line)
    print("Lower line:", lower_line)
    print("Left line:", left_line)
    
    return upper_line, lower_line, left_line

def hornet_length(picture : np.ndarray, picturefile : str) -> tuple:
    
    """Détermine la longueur du frelon en mm
    
    Args:
        picture (np.ndarray): Matrice de l'image binaire du frelon
        picturefile (str): Chemin d'accès à l'image, permet la génération de schémas d'analyse

    Returns:
        tuple : Longueur du frelon en pixels, coordonnées de l'extrémité de l'abdomen
    """
    # Génération d'une copie de la matrice de l'image binaire du frelon pour pouvoir la manipuler
    array_image = np.asarray(picture)
    
    # Récupération des dimensions
    number_of_lines = array_image.shape[0]
    number_of_columns = array_image.shape[1]
    
    # Recupération des lignes/colonnes délimitant de la zone d'analyse du frelon
    upper_line, lower_line, left_line = bounding_lines(array_image)
    
    # Extraction de la zone d'analyse du frelon pour gagner en performance
    extracted_array = array_image[upper_line:lower_line, left_line:number_of_columns]
    
    # Création et remplissage d'un tableau contenant le nombre de pixels noirs par ligne
    pixel_count_list = list()
    for line in extracted_array:
        pixel_count_list.append(zero_pixels(line))

    # Recupération de la ligne de longueur maximale et de son index dans la matrice originale
    # Gestion d'exception dans le cas ou aucune ligne n'est détectée
    try:
        pixel_count = np.max(pixel_count_list)
    except ValueError:
        print("No pixels found")
        pixel_count = 0
    
    if pixel_count == 0:
        index_max = 0
        sting_coordinates = (0, 0)
    else:
        index_max = pixel_count_list.index(pixel_count)
        sting_coordinates = int(left_line + pixel_count), index_max + upper_line
    
    # Schéma optionnel de démonstration
    #result_plot(picture, lower_line, upper_line, left_line, index_max, pixel_count, number_of_lines, number_of_columns, picturefile)
    
    print("Pixel count:", pixel_count)
    length_value = pixel_count
    
    return length_value, sting_coordinates