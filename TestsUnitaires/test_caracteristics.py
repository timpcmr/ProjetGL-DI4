import numpy as np
import cv2

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
    im1 = cv2.imread("Footage/hornetcube_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread("Footage/15_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    
    assert hl.bounding_lines(np.ones((1920, 1080)) * 255) == (1920, 0, 1080) # S'arrête à la dernière ligne
    assert hl.bounding_lines(np.zeros((1920, 1080))) == (1, 1919, 1) # S'arrête à la première ligne de pixels noirs
    assert hl.bounding_lines(im1) == (408, 687, 96)
    
    # La valeur exacte est (430, 621, 168) mais par la compression jpg pour enregistrer l'exemple, on obtient (433, 615, 169)
    # Cela n'arrive pas sur les exemple précédents car leur géométrie est plus simple
    valeur = hl.bounding_lines(im2)
    assert (valeur[0] in range (430,434)) and (valeur[1] in range (615, 622)) and (valeur [2] in range (168, 170))

def test_hornet_length():
    im1 = cv2.imread("Footage/black.png", cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread("Footage/white.png", cv2.IMREAD_GRAYSCALE)
    im3 = cv2.imread("Footage/bw50.png", cv2.IMREAD_GRAYSCALE)
    im4 = cv2.imread("Footage/hornetcube_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    im5 = cv2.imread("Footage/15_cutout.jpg", cv2.IMREAD_GRAYSCALE)
    
    #assert hl.hornet_length(im1, "Footage/black.png")[0] in range (1919, 1921)
    assert hl.hornet_length(im2, "Footage/white.png")[0] == 0
    #assert hl.hornet_length(im3, "Footage/bw50.png")[0] in range (959, 961)
    #assert hl.hornet_length(im4, "Footage/hornetcube_cutout.jpg")[0] in range(873, 875)
    #assert hl.hornet_length(im5, "Footage/15_cutout.jpg")[0] in range (707, 709)


# Section 2 : Test des fonctions de recherche de la forme de l'abdomen


