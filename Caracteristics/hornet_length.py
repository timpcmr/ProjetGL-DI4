import numpy as np
import cv2
# Returns the length of the hornet in terms of pixel count

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
    
    # Drawing the lines on the image
    
    picture = cv2.cvtColor(picture, cv2.COLOR_GRAY2BGR)
    
    # Lower line
    cv2.line(picture, (0, lower_line), (number_of_columns, lower_line), (0, 0, 255), 2)
    
    # Upper line
    cv2.line(picture, (0, upper_line), (number_of_columns, upper_line), (0, 0, 255), 2)
    
    # Left line
    cv2.line(picture, (left_line, 0), (left_line, number_of_lines), (0, 0, 255), 2)
    
    # Right line
    
    positionning = int(left_line + pixel_count)
    cv2.line(picture, (positionning, 0), (positionning, number_of_lines), (0, 0, 255), 2)
    
    # Longest line
    cv2.line(picture, (left_line, index_max + upper_line), (positionning, index_max + upper_line), (0, 255, 0), 2)
    
    # Sting
    cv2.circle(picture, (positionning, index_max + upper_line), 10, (255, 75, 0), -1)
    
    cv2.imshow("Hornet length", picture)
    
    # Exporting the plot
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
    
    # Getting the number of lines and columns of the image
    number_of_lines = array_image.shape[0]
    number_of_columns = array_image.shape[1]
    
    print("Number of lines:", number_of_lines)
    
    # Finding the lower horizontal line to frame the hornet
    counter = number_of_lines
    pixel_count = 0
    
    horizontal_number = array_image.shape[1] * 0.4
    while pixel_count < horizontal_number and counter > 0:
        pixel_count = zero_pixels(array_image[counter - 1])
        counter -= 1
    
    lower_line = counter
    
    # Finding the upper horizontal line to frame the hornet
    
    counter = 0
    pixel_count = 0
    
    while pixel_count < horizontal_number and counter < number_of_lines:
        pixel_count = zero_pixels(array_image[counter])
        counter += 1
    
    upper_line = counter
    
    # Finding the left vertical line to frame the hornet
    
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
    # Generating a copy of the picture to draw on
    array_image = np.asarray(picture)
    
    # Getting its dimensions
    number_of_lines = array_image.shape[0]
    number_of_columns = array_image.shape[1]
    
    # Getting the bounds of the area to analyze
    upper_line, lower_line, left_line = bounding_lines(array_image)
    
    # Extracting the area of interest to save computing time
    extracted_array = array_image[upper_line:lower_line, left_line:number_of_columns]
    
    # Making a list of the number of black pixels per line
    pixel_count_list = list()
    for line in extracted_array:
        pixel_count_list.append(zero_pixels(line))

    # Gettint its maximum value and its index in the original array
    
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
    
    # Optionnal plot : See the results of the analysis in a graphical manner
    #result_plot(picture, lower_line, upper_line, left_line, index_max, pixel_count, number_of_lines, number_of_columns, picturefile)
    
    print("Pixel count:", pixel_count)
    length_value = pixel_count
    
    return length_value, sting_coordinates