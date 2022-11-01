import cv2  # Computer vision library

# Read the color image
import numpy as np


# Function that take a mask image in first parameter and calculate contours in order to draw a bounding box to run the
# grabcut algorithm, the second parameter correspond to the original image to grabcut
def boundingbox(mask, filename):
    image = cv2.imread(mask)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Display the grayscale image
    '''
    cv2.imshow('Gray image', gray)
    cv2.waitKey(0)  # Wait for keypress to continue
    cv2.destroyAllWindows()  # Close windows
    '''

    # Convert the grayscale image to binary
    ret, binary = cv2.threshold(gray, 100, 255,
                                cv2.THRESH_OTSU)

    # Display the binary image
    '''
    cv2.imshow('Binary image', binary)
    cv2.waitKey(0)  # Wait for keypress to continue
    cv2.destroyAllWindows()  # Close windows
    '''

    # Find the contours on the inverted binary image, and store them in a list
    # Contours are drawn around white blobs.
    # hierarchy variable contains info on the relationship between the contours
    contours, hierarchy = cv2.findContours(binary,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours (in red) on the original image
    # -1 means to draw all contours
    with_contours = cv2.drawContours(image, contours, -1, (255, 0, 255), 3)

    height, width, _ = image.shape
    min_x, min_y = width, height
    max_x = max_y = 0

    # Draw a bounding box containing all contours
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

        min_x, max_x = min(x, min_x), max(x + w, max_x)
        min_y, max_y = min(y, min_y), max(y + h, max_y)

    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(with_contours, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

    # Show all contours detected and the rectangle drawn that contains all the contours
    # It's possible to comment these 3 lines if you don't want to show these results
    cv2.imshow('All contours with bounding box', with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    new_image = cv2.imread(filename)

    # Create a 0's mask
    mask = np.zeros(new_image.shape[:2], np.uint8)
    # Create 2 arrays for background and foreground model
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    # Create the rect tuple for openCV Grabcut
    rect = (min_x, min_y, abs(min_x - max_x), abs(min_y - max_y))

    mask, bgdModel, fgdModel = cv2.grabCut(new_image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    output = new_image * mask2[:, :, np.newaxis]

    # Computing ratio of the color range Orange/Yellow
    ratio = cv2.countNonZero(mask2) / (new_image.size / 3)
    print('pixel percentage of the size of the Asians hornet:', np.round(ratio * 100, 2))

    cv2.imshow('Grabcut output', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
