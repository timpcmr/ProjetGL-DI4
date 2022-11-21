
import sys
import time
import cv2

from Cut_Out.cutout import cutout
from Caracteristics.hornet_class import hornet_class
from XMLgenerator.xmlgenerator import xmlgenerator

def main() -> int:
    
    
    time_start = time.process_time()
    
    ############ Get the image to analyse ############
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_path>")
        return
    
    # Get the image path and the trap reference
    else :
        picturefile = sys.argv[1]
        try:
            trap_reference = sys.argv[2]
        except:
            trap_reference = "UNDEFINED"
    
    
    ############ Getting a cut out version of the image ############
    
    try :
        hornet_binary_mask = cutout(picturefile)
    except FileNotFoundError:
        print("Could not read the image.")
        return 1
    
    ############ Getting the caracteristics of the hornet ############
    
    hclass = hornet_class(hornet_binary_mask, picturefile)
    
    ############ Generating the XML file ############
    
    test = {"cast" : "Fondatrice", "hornetlength" : "10", "abdomenshape" : "Rond"}
    
    #xmlgenerator(test, picturefile, trap_reference)
    
    
    time_end = time.process_time()
    compute_time = time_end - time_start
    print("Time to compute: ", compute_time, "s")
    
    return 0

if __name__ == "__main__":
    main()