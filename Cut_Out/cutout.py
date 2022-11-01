
import cv2
from .boundingbox import *
from .colour_mask import *


# Should be launch with the terminal by putting the image to analyse in first parameter
def cutout(filename : str):
    # Loading images
    img = cv2.imread(filename)
    imagename = filename.removeprefix("Footage/")

    colour_mask(img, imagename)
    boundingbox('Footage/cutout_versions/Mask/' + imagename, filename, imagename)
