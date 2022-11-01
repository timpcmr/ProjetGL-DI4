import string
import cv2
from boundingbox import *
from colour_mask import *


# Should be launch with the terminal by putting the image to analyse in first parameter
def cutout(filename : string):
    # Loading images
    img = cv2.imread(filename)
    print(type(img))

    colour_mask(img)
    boundingbox("Hornet_mask.jpg", filename)
