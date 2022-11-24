import numpy as np
import cv2
from PIL import Image
from PIL.Image import fromarray

def abdomen_shape(picture_array : np.ndarray, sting_coordinates : tuple) -> str:
    im_sting = picture_array[sting_coordinates[1] - 100:sting_coordinates[1],
               sting_coordinates[0] - 100:sting_coordinates[0]]

    edged = cv2.Canny(im_sting, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    whiteblankimage = 255 * np.ones(shape=[100, 150, 3], dtype=np.uint8)

    cv2.drawContours(image=whiteblankimage, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=1,
                     lineType=cv2.LINE_AA)

    cv2.imwrite('Footage/Contour_dard.jpg', whiteblankimage)
    cv2.imshow('Contour_Dard', whiteblankimage)
    cv2.waitKey(0)

    dard = Image.open('Footage/Contour_dard.jpg')
    largeur, hauteur = dard.size
    X = []
    Y = []
    for x in range(largeur):
        for y in range(hauteur):
            if dard.getpixel((x, y)) == (0, 0, 0):
                X.append(x)
                Y.append(y)
    fonction = np.polyfit(X, Y, 1)
    poly = np.poly1d(fonction)

    print(X,Y)
    print(poly)