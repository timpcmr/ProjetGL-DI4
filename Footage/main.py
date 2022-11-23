import cv2
import time

if __name__ == '__main__':
    timestrat = time.process_time()
    img = cv2.imread('15_cutout.jpg', cv2.IMREAD_GRAYSCALE)
    #smooth = cv2.erode(img, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), img)
    img_o = cv2.morphologyEx(img, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    img_c = cv2.morphologyEx(img_o, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4)))
    end = time.process_time()
    t = end - timestrat
    print(t , "s")