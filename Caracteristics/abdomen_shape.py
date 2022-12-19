import cv2
import numpy as np
from PIL import Image
import math
import os


def abdomen_shape(picture_array : np.ndarray, sting_coordinates : tuple) -> str:

    """Détermine la forme de l'abdomen du frelon. Par extension, on peut déterminer le sexe de l'insecte.
    
    Args:
        picture_array (np.ndarray): Matrice du masque binaire du frelon
        sting_coordinates (tuple): Coordonnées de l'extremité de l'abdomen
        
    Returns:
        str: Résultat de la forme de l'abdomen
    """

    #Taille de l'image
    taille = picture_array.shape
    longueur_tot = taille[0]
    largeur_tot = taille[1]

    #Zoom sur la moitié haute de l'abdomen
    im_sting = picture_array[sting_coordinates[1] - int(largeur_tot*0.05):sting_coordinates[1],
               sting_coordinates[0] - int(longueur_tot*0.05):sting_coordinates[0]]

    #Création des contours
    edged = cv2.Canny(im_sting, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #Création d'une image blanche
    whiteblankimage = 255 * np.ones(shape=[int(longueur_tot*0.05), int(largeur_tot*0.05), 3], dtype=np.uint8)

    #Dessin des contours sur l'image blanche
    cv2.drawContours(image=whiteblankimage, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=1,
                     lineType=cv2.LINE_AA)

    cv2.imwrite('Footage/Contour_dard_haut.jpg', whiteblankimage)

    #Calculs
    X1,Y1= find_points('Footage/Contour_dard_haut.jpg')
    if X1 == [] or Y1 == []:
        return
    if len(X1) == longueur_tot*largeur_tot or len(Y1) == longueur_tot*largeur_tot:
        return
    m1 = find_coeffs(X1,Y1)

    #Zoom sur la moitié basse de l'abdomen
    im_sting = picture_array[sting_coordinates[1]:sting_coordinates[1]+int(largeur_tot*0.05),
               sting_coordinates[0]-int(longueur_tot*0.05):sting_coordinates[0]]

    #Création des contours
    edged = cv2.Canny(im_sting, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #Création d'une image blanche
    whiteblankimage = 255 * np.ones(shape=[int(longueur_tot*0.05),int(largeur_tot*0.05), 3], dtype=np.uint8)

    #Dessin des contours sur l'image blanche
    cv2.drawContours(image=whiteblankimage, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=1,
                     lineType=cv2.LINE_AA)

    cv2.imwrite('Footage/Contour_dard_bas.jpg', whiteblankimage)

    #Calculs
    X2,Y2= find_points('Footage/Contour_dard_bas.jpg')
    if X2 == [] or Y2 == []:
        return
    if len(X2) == longueur_tot*largeur_tot or len(Y2) == longueur_tot*largeur_tot:
        return

    m2 = find_coeffs(X2,Y2)
    
    os.remove('Footage/Contour_dard_haut.jpg')
    os.remove('Footage/Contour_dard_bas.jpg')

    #Calcul de l'angle
    angle = find_angle(m1,m2)
    #Détermination de la forme de l'abdomen
    if angle <= 60:
        print("pointu d'après l'angle")
        resultat_angle = "pointu"
    if angle > 60:
        print("rond d'après l'angle")
        resultat_angle = "rond"

    #Méthode 2 : comparaison avec une fonction logarithmique et une fonction affine
    #Affine
    fonction_affine = np.polyfit(X1, Y1, 1)
    moyenne_diff_affine = difference_moyenne_affine(X1, Y1, fonction_affine)

    #Logarithmique
    fonction_log = np.polyfit(X1, np.log(Y1), 1)
    moyenne_diff_log = difference_moyenne_log(X1, Y1, fonction_log)

    #Comparaison des résultats
    if moyenne_diff_affine < moyenne_diff_log:
        print("pointu d'après la moyenne")
        resultat_comparaison = "pointu"
    if moyenne_diff_affine > moyenne_diff_log:
        print("rond d'après la moyenne")
        resultat_comparaison = "rond"

    #Résultat final
    if resultat_angle == resultat_comparaison:
        return resultat_comparaison #On renvoie le résultat commun aux deux méthodes
    if resultat_angle != resultat_comparaison:
        return resultat_angle #On choisit de donner la forme de l'abdomen d'après l'angle car plus fiable





def find_points(picturepath : str) -> list:
    """Trouve la fonction de la droite de l'abdomen du frelon.

    Args:
        picturepath (str): Chemin du contour de l'abdomen du frelon

    Returns:
        list: Liste des coefficients de la fonction
    """
    im = Image.open(picturepath)
    largeur, hauteur = im.size
    X = []
    Y = []
    for x in range(largeur):
        for y in range(hauteur):
            if im.getpixel((x, y)) == (0, 0, 0):
                X.append(x)
                Y.append(y)
    return X,Y


def find_coeffs(X : list, Y : list) -> list:
    """Trouve les coefficients de la fonction de la droite de l'abdomen du frelon.

    Args:
        X (list): Liste des abscisses des points de la droite
        Y (list): Liste des ordonnées des points de la droite

    Returns:
        list: Coefficients de la fonction
    """
    fonction = np.polyfit(X, Y, 1)
    poly = np.poly1d(fonction)
    return poly.coeffs


def find_angle(coeff1 : list, coeff2 : list) -> float:
    """Trouve l'angle entre deux droites.

    Args:
        coeff1 (list): Coefficients de la première droite
        coeff2 (list): Coefficients de la deuxième droite

    Returns:
        float: Angle entre les deux droites
    """
    tan = (coeff1[0] - coeff2[0])/(1 + coeff1[0]*coeff2[0])
    arctan = np.arctan(tan)
    degre = arctan * 180 / math.pi
    return degre

def difference_moyenne_affine(X : list, Y : list, coeff : list) -> float:
    """Trouve la différence moyenne entre les points trouvés et la fonction affine.

    Args:
        X (list): Liste des abscisses des points
        Y (list): Liste des ordonnées des points
        coeff (list): Coefficients de la fonction affine

    Returns:
        float: Différence moyenne entre les points et la fonction affine
    """
    Y_diff = []
    diff = 0
    for i in range(len(X)):
        Y_i = coeff[0]*i + coeff[1]
        Y_diff.append(Y_i)
        diff = (Y_diff[i] + Y[i]) / 2
    for i in range(len(Y_diff)):
        diff_total = diff + Y_diff[i]
    Moyenne_diff = diff_total / len(Y_diff)
    return Moyenne_diff

def difference_moyenne_log(X : list, Y : list, coeff : list) -> float:
    """Trouve la différence moyenne entre les points trouvés et la fonction logarithmique.

    Args:
        X (list): Liste des abscisses des points
        Y (list): Liste des ordonnées des points
        coeff (list): Coefficients de la fonction logarithmique

    Returns:
        float: Différence moyenne entre les points et la fonction logarithmique
    """
    Y_diff = []
    diff = 0
    for i in range(len(X)):
        if i == 0:
            Y_i = Y[0]
        else:
            Y_i = coeff[0]*np.log(i) + coeff[1]
        Y_diff.append(Y_i)
        diff = (Y_diff[i] + Y[i]) / 2
    for i in range(len(Y_diff)):
        diff_total = diff + Y_diff[i]
    Moyenne_diff = diff_total / len(Y_diff)
    return Moyenne_diff