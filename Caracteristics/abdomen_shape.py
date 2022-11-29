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
    
    im_sting = picture_array[sting_coordinates[1] - 100:sting_coordinates[1],
               sting_coordinates[0] - 100:sting_coordinates[0]]

    edged = cv2.Canny(im_sting, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    whiteblankimage = 255 * np.ones(shape=[100, 150, 3], dtype=np.uint8)

    cv2.drawContours(image=whiteblankimage, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=1,
                     lineType=cv2.LINE_AA)

    cv2.imwrite('Footage/Contour_dard_haut.jpg', whiteblankimage)
    cv2.imshow('Contour_Dard_haut', whiteblankimage)
    cv2.waitKey(0)

    dard_up = Image.open('Footage/Contour_dard_haut.jpg')
    largeur, hauteur = dard_up.size
    X1 = []
    Y1 = []
    for x in range(largeur):
        for y in range(hauteur):
            if dard_up.getpixel((x, y)) == (0, 0, 0):
                X1.append(x)
                Y1.append(y)
    fonction1 = np.polyfit(X1, Y1, 1)
    poly1 = np.poly1d(fonction1)

    print(X1,Y1)
    print(poly1)
    m1= poly1.coeffs
    print(m1)

    im_sting = picture_array[sting_coordinates[1]:sting_coordinates[1]+100,
               sting_coordinates[0]-100:sting_coordinates[0]]

    edged = cv2.Canny(im_sting, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    whiteblankimage = 255 * np.ones(shape=[100, 150, 3], dtype=np.uint8)

    cv2.drawContours(image=whiteblankimage, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=1,
                     lineType=cv2.LINE_AA)

    cv2.imwrite('Footage/Contour_dard_bas.jpg', whiteblankimage)
    cv2.imshow('Contour_Dard_bas', whiteblankimage)
    cv2.waitKey(0)

    dard_down = Image.open('Footage/Contour_dard_bas.jpg')
    largeur, hauteur = dard_down.size
    X2 = []
    Y2 = []
    for x in range(largeur):
        for y in range(hauteur):
            if dard_down.getpixel((x, y)) == (0, 0, 0):
                X2.append(x)
                Y2.append(y)
    fonction2 = np.polyfit(X2, Y2, 1)
    poly2 = np.poly1d(fonction2)

    print(X2, Y2)
    print(poly2)
    m2 = poly2.coeffs
    print(m2)

    tan = (m1[0] - m2[0])/(1 + m1[0]*m2[0])
    arctan = np.arctan(tan)
    degre = arctan * 180 / math.pi
    print(degre)

    if degre <= 90:
        print("pointu")
        return "pointu"
    if degre > 90:
        print("rond")
        return "rond"