import cv2
import numpy as np

# Importation des fonctions du programme
import main as prog

def test_cutout():
    im1 = "Footage/white.png"
    im2 = "Footage/black.png"
    im3 = "Footage/bw50.png"
    r_im3 = prog.cutout(im3)
    
    assert np.array_equal(prog.cutout(im1), (np.ones((1920, 1080)) * 255).astype(np.uint8))
    assert np.array_equal(prog.cutout(im2), np.zeros((1920, 1080)).astype(np.uint8))
    assert np.array_equal(r_im3[:][:960], np.ones((960, 1080)).astype(np.uint8) * 255) & np.array_equal(r_im3[:][960:], np.zeros((960, 1080)).astype(np.uint8))


