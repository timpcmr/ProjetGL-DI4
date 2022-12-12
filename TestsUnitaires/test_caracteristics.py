import numpy as np
import cv2
import os

import Caracteristics.hornet_length as hl
import Caracteristics.hornet_class as hc

# Les intervalles de valeurs (in range) sont présents pour tenir compte des erreurs d'arrondis et de la compression de l'image

# Section 1 : Test des fonctions de recherche de la longeur

def test_zero_pixels():
    assert hl.zero_pixels(np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])) == 9
    assert hl.zero_pixels(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])) == 10
    assert hl.zero_pixels(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])) == 9
    assert hl.zero_pixels(np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0])) == 9
    assert hl.zero_pixels(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])) == 0

def test_bounding_lines():
    
    # Chargement des images de référence
    im1 = cv2.imread("Footage/hornetcube_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread("Footage/15_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    
    # Nettoyage des artéfacts de la compression jpg
    im1 = cv2.threshold(im1, 125, 255, cv2.THRESH_BINARY)[1]
    im2 = cv2.threshold(im2, 125, 255, cv2.THRESH_BINARY)[1]
    
    # Tests
    assert hl.bounding_lines(np.ones((1920, 1080)) * 255) == (1920, 0, 1080) # S'arrête à la dernière ligne
    assert hl.bounding_lines(np.zeros((1920, 1080))) == (1, 1919, 1) # S'arrête à la première ligne de pixels noirs
    assert hl.bounding_lines(im1) == (408, 687, 96)
    assert hl.bounding_lines(im2) == (430, 621, 168)

def test_hornet_length():
    
    # Chargement des images de référence
    im1 = cv2.imread("Footage/black.png", cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread("Footage/white.png", cv2.IMREAD_GRAYSCALE)
    im3 = cv2.imread("Footage/bw50.png", cv2.IMREAD_GRAYSCALE)
    im4 = cv2.imread("Footage/hornetcube_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    im5 = cv2.imread("Footage/15_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    
    
    # Nettoyage des artéfacts de la compression jpg
    im1 = cv2.threshold(im1, 125, 255, cv2.THRESH_BINARY)[1]
    im2 = cv2.threshold(im2, 125, 255, cv2.THRESH_BINARY)[1]
    im3 = cv2.threshold(im3, 125, 255, cv2.THRESH_BINARY)[1]
    im4 = cv2.threshold(im4, 125, 255, cv2.THRESH_BINARY)[1]
    im5 = cv2.threshold(im5, 125, 255, cv2.THRESH_BINARY)[1]
    
    # Tests
    assert hl.hornet_length(im1, "Footage/black.png")[0] == 1919
    assert hl.hornet_length(im2, "Footage/white.png")[0] == 0
    assert hl.hornet_length(im3, "Footage/bw50.png")[0] == 959
    assert hl.hornet_length(im4, "Footage/hornetcube_cutout.jpg")[0] == 874
    assert hl.hornet_length(im5, "Footage/15_cutout.jpg")[0] == 708


# Section 2 : Test des fonctions de recherche de la forme de l'abdomen
def test_find_points():

    # Chargement des images de référence
    im1 = "Footage/abdomen_up.jpg"
    im2 = "Footage/abdomen_down.jpg"
    im3 = "Footage/white.png"

    # Tests
    assert hc.find_points(im1) == ([4, 10, 14, 15, 45, 55, 61, 62, 63, 65, 66, 75, 81, 83, 84, 93, 95], [19, 20, 22, 24, 36, 48, 53, 54, 56, 57, 58, 67, 77, 79, 82, 91, 97])
    assert hc.find_points(im2) == ([10, 15, 21, 27, 34, 42, 49, 51, 61, 66, 69, 72, 74, 75, 78, 96], [75, 73, 71, 69, 67, 65, 57, 55, 49, 44, 42, 39, 37, 36, 33, 15])
    assert hc.find_points(im3) == ([], [])

def test_find_coeffs():

    # Tests (on arrondi car la fonction appelé donne des résultats avec une précision de 10^-15)
    # Exemple : Donne 1.9999999999999998 au lieu de 2
    assert round(hc.find_coeffs([1, 2, 3], [1, 2, 3])[0]) == 1
    assert round(hc.find_coeffs([1, 2, 3], [1, 2, 3])[1]) == 0
    assert round(hc.find_coeffs([1, 2, 3], [2, 4, 6])[0]) == 2
    assert round(hc.find_coeffs([1, 2, 3], [2, 4, 6])[1]) == 0
    assert round(hc.find_coeffs([1, 2, 3], [4, 7, 10])[0]) == 3
    assert round(hc.find_coeffs([1, 2, 3], [4, 7, 10])[1]) == 1
    assert round(hc.find_coeffs([4, 10, 12.5], [0, 12, 17])[0]) == 2
    assert round(hc.find_coeffs([4, 10, 12.5], [0, 12, 17])[1]) == -8

def test_find_angle():

    # Tests
    assert hc.find_angle((2,4), (-3,8)) == -45
    assert hc.find_angle((10,-25), (4,8)) == 8.325650330426836
    assert hc.find_angle((0,0), (0,0)) == 0
    assert hc.find_angle((2000,3000), (5,9)) == 11.281284586650996
    assert hc.find_angle((5,-5), (1,1)) == 33.690067525979785

def test_abdomen_shape():

    # Chargement des images de référence
    im1 = cv2.imread("Footage/15_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread("Footage/white.png", cv2.IMREAD_GRAYSCALE)
    im3 = cv2.imread("Footage/black.png", cv2.IMREAD_GRAYSCALE)
    im4 = cv2.imread("Footage/Round.png", cv2.IMREAD_GRAYSCALE)
    im5 = cv2.imread("Footage/Triangle.png", cv2.IMREAD_GRAYSCALE)


    # Tests
    assert hc.abdomen_shape(im1,(876, 535)) == "pointu"
    assert hc.abdomen_shape(im2,(971, 533)) == None # Pas de forme (tout blanc)
    assert hc.abdomen_shape(im3,(500, 500)) == None # Pas de forme (tout noir)
    assert hc.abdomen_shape(im4,(994, 482)) == "rond"
    assert hc.abdomen_shape(im5,(1000, 457)) == "pointu"



    # Suppression des fichiers temporaires
    os.remove("Footage/Contour_dard_haut.jpg")
    os.remove("Footage/Contour_dard_bas.jpg")

def test_difference_moyenne_affine():
        assert hc.difference_moyenne_affine([1,2,3],[1,2,3], (1, 0)) == 1.5
        assert hc.difference_moyenne_affine([5,9,12],[45,50,53], (2, 0)) == 10.833333333333334
        assert hc.difference_moyenne_affine([12,15,20],[34,1,23], (3, 0)) == 6.833333333333333

def test_difference_moyenne_log():
        assert hc.difference_moyenne_log([1,2,3],[1,2,3], (1, 0)) == 0.8465735902799727
        assert hc.difference_moyenne_log([5,9,12],[45,50,53], (2, 0)) == 9.526480513893278
        assert hc.difference_moyenne_log([12,15,20],[34,1,23], (3, 0)) == 4.873054104173251