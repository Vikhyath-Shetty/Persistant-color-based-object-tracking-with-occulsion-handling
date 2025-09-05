from cv2.typing import MatLike
import cv2 as cv
import numpy as np

def calculate_histogram(frame: MatLike, contour:np.ndarray):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    object = np.zeros(hsv.shape[:2],dtype=np.uint8)
    cv.drawContours(object,[contour],-1,(255,255,255),-1)
    kernal = cv.getStructuringElement(cv.MORPH_RECT,(5,5))
    object = cv.morphologyEx(object,cv.MORPH_CLOSE,kernal)
    object = cv.morphologyEx(object,cv.MORPH_OPEN,kernal)
    hist = cv.calcHist([hsv],[0,1],object,[30,32], [0,180,0,256])
    cv.normalize(hist, hist, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    return hist