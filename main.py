
import sys
import time

from Cut_Out.cutout import cutout
from Caracteristics.hornet_class import *

def main():
    
    time_start = time.process_time()
    
    ############ Get the image to analyse ############
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_path>")
        return
    
    else :
        picturefile = sys.argv[1]
    
    ############ Getting a cut out version of the image ############
    
    cutout(picturefile)
    
    
    time_end = time.process_time()
    compute_time = time_end - time_start
    print("Time to compute: ", compute_time, "s")
    
main()