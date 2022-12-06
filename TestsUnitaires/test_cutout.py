import numpy as np
import cv2

# Importation des fonctions du programme
import Cut_Out.cutout as prog

def test_cutout():
    im1 = "Footage/white.png"
    im2 = "Footage/black.png"
    im3 = "Footage/bw50.png"
    r_im3 = prog.cutout(im3)
    
    a1 = np.multiply(np.ones((1920, 1080), dtype="uint8"), 255)
    a2 = np.zeros((1920, 1080), dtype="uint8")
    a3 = np.ones((960, 1080)) * 255
    a4 = np.zeros((960, 1080)).astype(np.uint8)
    
    # Elimination des artéfacts de la compression jpg
    a1 = cv2.threshold(a1, 254, 255, cv2.THRESH_BINARY)[1]
    a2 = cv2.threshold(a2, 125, 255, cv2.THRESH_BINARY)[1]
    a3 = cv2.threshold(a3, 125, 255, cv2.THRESH_BINARY)[1]
    a4 = cv2.threshold(a4, 125, 255, cv2.THRESH_BINARY)[1]
    
    assert np.array_equal(prog.cutout(im1), a1)
    assert np.array_equal(prog.cutout(im2), a2)
    assert np.array_equal(r_im3[:][:960], a3) and np.array_equal(r_im3[:][960:], a4)


