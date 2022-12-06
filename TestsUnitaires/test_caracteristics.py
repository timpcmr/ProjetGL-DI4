import numpy as np
import cv2

import main as prog

# Section 1 : Test des fonctions de recherche de la longeur

def test_zero_pixels():
    assert prog.zero_pixels(np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])) == 9
    assert prog.zero_pixels(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])) == 10
    assert prog.zero_pixels(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])) == 9
    assert prog.zero_pixels(np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0])) == 9
    assert prog.zero_pixels(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])) == 0

def test_bounding_lines():
    im1 = cv2.imread("Footage/hornetcube_cutout.jpg", cv2.LOAD_IMAGE_GRAYSCALE)
    im2 = cv2.imread("Footage/15_cutout.jpg", cv2.LOAD_IMAGE_GRAYSCALE)
    
    assert prog.bounding_lines(np.ones((1920, 1080)) * 255) == (1920, 0, 1080)
    assert prog.bounding_lines(np.zeros((1920, 1080))) == (0, 1920, 0)
    assert prog.bounding_lines(im1) == (408, 687, 96)
    assert prog.bounding_lines(im2) == (430, 621, 168)

def test_hornet_length():
    im1 = cv2.imread("Footage/black.png", cv2.LOAD_IMAGE_GRAYSCALE)
    im2 = cv2.imread("Footage/white.png", cv2.LOAD_IMAGE_GRAYSCALE)
    im3 = cv2.imread("Footage/bw50.png", cv2.LOAD_IMAGE_GRAYSCALE)
    im4 = cv2.imread("Footage/hornetcube_cutout.jpg", cv2.LOAD_IMAGE_GRAYSCALE)
    im5 = cv2.imread("Footage/15_cutout.jpg", cv2.LOAD_IMAGE_GRAYSCALE)
    
    assert prog.hornet_length(im1, "Footage/black.png") == 1920
    assert prog.hornet_length(im2, "Footage/white.png") == 0
    assert prog.hornet_length(im3, "Footage/bw50.png") == 960
    assert prog.hornet_length(im4, "Footage/hornetcube_cutout.jpg") == 874
    assert prog.hornet_length(im5, "Footage/15_cutout.jpg") == 708


# Section 2 : Test des fonctions de recherche de la forme de l'abdomen


