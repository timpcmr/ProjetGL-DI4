from .abdomen_shape import *
from .hornet_length import *
import cv2

def hornet_class(RGBApicture, picturefile):
    
    hornet_length_value, index_line_sting = hornet_length(RGBApicture, picturefile)
    
    
    return dict