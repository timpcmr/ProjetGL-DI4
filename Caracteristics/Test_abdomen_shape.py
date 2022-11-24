import numpy as np
import cv2

def Test_abdomen_shape():
    print("Début")
    # Lecture image
    image = cv2.imread('test.jpg')
    cv2.waitKey(0)

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Coins
    edged = cv2.Canny(gray, 30, 200)
    cv2.waitKey(0)

    # Recherche des contours
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.imshow('Contours', edged)
    cv2.waitKey(0)

    # Dessin des contours
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    cv2.imshow('Contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

Test_abdomen_shape()