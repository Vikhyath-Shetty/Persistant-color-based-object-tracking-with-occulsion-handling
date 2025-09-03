from typing import List
import cv2 as cv
from cv2.typing import MatLike
from utils import calculate_histogram
import numpy as np
import matplotlib.pyplot as plt

class DetectedObject:
    def __init__(self, frame: MatLike, contour:np.ndarray) -> None:
        self.x,self.y,self.w,self.h = cv.boundingRect(contour)
        self.frame_count = 0
        self.centroid = (self.x+self.w)//2,(self.y+self.h)//2
        self.histogram = calculate_histogram(frame,contour)

        

    
