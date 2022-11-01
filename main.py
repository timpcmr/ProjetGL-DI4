from Cut_Out.cutout import *
import sys

from Cut_Out.cutout import cutout

def main():
    
    ############ Get the image to analyse ############
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_path>")
        return
    
    else :
        picturefile = sys.argv[1]
    
    ############ Getting a cut out version of the image ############
    
    cutout(picturefile)
    
    
main()