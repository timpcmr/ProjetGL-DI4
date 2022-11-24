from .abdomen_shape import *
from .hornet_length import *
import cv2

def hornet_class(hornet_binary_mask : np.ndarray, picturefile : str) -> dict:
    
    # initialising the output variable
    caracteristics = dict()
    
    # Determining the hornet length
    hornet_length_value, sting_coordinates = hornet_length(hornet_binary_mask, picturefile)
    caracteristics["hornetlength"] = hornet_length_value
    
    # determinining the abdomen shape
    abdomen_shape_value = abdomen_shape(hornet_binary_mask, sting_coordinates)
    caracteristics["abdomenshape"] = abdomen_shape_value
    
    
    
    return caracteristics