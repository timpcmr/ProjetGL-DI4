import cv2
import numpy as np
from PIL import Image
import math


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
    print("taille :",longueur_tot,largeur_tot)

    #Zoom sur la moitié haute de l'abdomen
    im_sting = picture_array[sting_coordinates[1] - int(largeur_tot*0.1):sting_coordinates[1],
               sting_coordinates[0] - int(longueur_tot*0.1):sting_coordinates[0]]

    #Création des contours
    edged = cv2.Canny(im_sting, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #Création d'une image blanche
    whiteblankimage = 255 * np.ones(shape=[int(longueur_tot*0.1), int(largeur_tot*0.1), 3], dtype=np.uint8)

    #Dessin des contours sur l'image blanche
    cv2.drawContours(image=whiteblankimage, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=1,
                     lineType=cv2.LINE_AA)

    cv2.imshow('Avant contours', im_sting)
    cv2.imwrite('Footage/Contour_dard_haut.jpg', whiteblankimage)
    cv2.imshow('Contour_Dard_haut', whiteblankimage)
    cv2.waitKey(0)

    #Calculs
    X1,Y1= find_points('Footage/Contour_dard_haut.jpg')
    m1 = find_coeffs(X1,Y1)
    print("coeffs : ",m1)

    #Zoom sur la moitié basse de l'abdomen
    im_sting = picture_array[sting_coordinates[1]:sting_coordinates[1]+int(largeur_tot*0.1),
               sting_coordinates[0]-int(longueur_tot*0.1):sting_coordinates[0]]

    #Création des contours
    edged = cv2.Canny(im_sting, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #Création d'une image blanche
    whiteblankimage = 255 * np.ones(shape=[int(longueur_tot*0.1),int(largeur_tot*0.1), 3], dtype=np.uint8)

    #Dessin des contours sur l'image blanche
    cv2.drawContours(image=whiteblankimage, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=1,
                     lineType=cv2.LINE_AA)

    cv2.imwrite('Footage/Contour_dard_bas.jpg', whiteblankimage)
    cv2.imshow('Contour_Dard_bas', whiteblankimage)
    cv2.waitKey(0)

    #Calculs
    X2,Y2= find_points('Footage/Contour_dard_bas.jpg')
    m2 = find_coeffs(X2,Y2)
    print(m2)

    #Calcul de l'angle
    angle = find_angle(m1,m2)

    #Détermination de la forme de l'abdomen
    if angle <= 90:
        print("pointu")
        return "pointu"
    if angle > 90:
        print("rond")
        return "rond"


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