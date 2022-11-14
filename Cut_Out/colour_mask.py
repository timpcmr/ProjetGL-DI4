import cv2
import numpy as np


# Function that take an image in parameter and make the masks of colours between Orange to Yellow
# and between Brown to black. Also write a final mask in real colour
def colour_mask(img : np.ndarray, filename : str):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    color1 = (10, 200, 20)  # orange
    color2 = (28, 255, 255)  # yellow

    color3 = (0, 70 , 0)  # black
    color4 = (15, 200, 140)  # brown

    # Define threshold color range to filter
    mask1 = cv2.inRange(hsv_img, color1, color2)  # Mask for orange to yellow colors
    mask2 = cv2.inRange(hsv_img, color3, color4)  # Mask for brown to black colors

    # Bitwise-AND mask and original image
    resOrangeToYellow = cv2.bitwise_and(hsv_img, hsv_img, mask=mask1)
    resBrownToBlack = cv2.bitwise_and(hsv_img, hsv_img, mask=mask2)

    # Addition of the two masks
    res_hsv = cv2.addWeighted(resBrownToBlack, 1, resOrangeToYellow, 1, 0)
    res = res_hsv


    # Computing ratio of the color range Orange/Yellow and rounding to two decimal places
    ratioOfOrangeToYellow = cv2.countNonZero(mask1) / (hsv_img.size / 3)
    print('pixel percentage of colour Orange to Yellow:', np.round(ratioOfOrangeToYellow * 100, 2))

    # write the result of the colour mask res of the hornet in a file called Hornet_mask.jpg
    cv2.imwrite('Footage/cutout_versions/Mask/' + filename, res)
