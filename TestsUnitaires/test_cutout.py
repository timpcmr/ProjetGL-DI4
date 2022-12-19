import numpy as np
import cv2

# Importation des fonctions du programme
import Cut_Out.cutout as prog

def test_cutout():

    """Teste la génération du masque binaire du frelon.
    L'idée est, avec des images de référence, de vérifier que le masque binaire généré est bien celui attendu.
    """
    
    im1 = "Footage/white.png"
    im2 = "Footage/black.png"
    im3 = "Footage/bw50.png"
    r_im3 = prog.cutout(im3)
    
    # Création des images de référence (OpenCV inverse les axes)
    a1 = np.multiply(np.ones((1080, 1920), dtype="uint8"), 255)
    a2 = np.zeros((1080, 1920), dtype="uint8")
    a3 = np.ones((1080, 961), dtype="uint8") * 255
    a4 = np.zeros((1080, 959)).astype(np.uint8)
    
    # Elimination des artéfacts de la compression jpg
    a1 = cv2.threshold(a1, 125, 255, cv2.THRESH_BINARY)[1]
    a2 = cv2.threshold(a2, 125, 255, cv2.THRESH_BINARY)[1]
    a3 = cv2.threshold(a3, 125, 255, cv2.THRESH_BINARY)[1]
    a4 = cv2.threshold(a4, 125, 255, cv2.THRESH_BINARY)[1]
    
    assert np.array_equal(prog.cutout(im1), a1) # Image blanche, le masque binaire doit être blanc
    assert np.array_equal(prog.cutout(im2), a2) # Image noire, le masque binaire doit être noir
    
    # Image à 50% de blanc et de noir, le masque binaire doit être blanc à gauche et noir à droite
    assert np.array_equal(r_im3[:, :961], a3) 
    assert np.array_equal(r_im3[:, 961:], a4)


