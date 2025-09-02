from cv2.typing import MatLike
import cv2 as cv


def calculate_histogram(frame: MatLike, roi: MatLike):
    object = cv.bitwise_and(frame,frame,mask = roi)
    cv.imshow('object',object)
    histogram = cv.calcHist([frame], [0, 1],None, [30, 32], [0, 180, 0, 256])
    print(histogram)
    cv.normalize(histogram, histogram, 0, 255, cv.NORM_MINMAX)
    return histogram
