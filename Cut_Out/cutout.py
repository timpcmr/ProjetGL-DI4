
import cv2

# Should be launch with the terminal by putting the image to analyse in first parameter
def cutout(filename : str):
    # Loading images
    img = cv2.imread(filename)
    img_RGBA = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    img_GREY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    mask = cv2.threshold(img_GREY, 90, 255, cv2.THRESH_BINARY)
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mask[1][i][j] == 255:
                img_RGBA[i][j] = [0, 0, 0, 0]

    return img_RGBA
