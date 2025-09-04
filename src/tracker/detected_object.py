import cv2 as cv
from cv2.typing import MatLike
from utils import calculate_histogram
import numpy as np
from .kalman_filter import KalmanFilter


class DetectedObject:
    def __init__(self, frame: MatLike, contour:np.ndarray):
        self.frame = frame
        self.contour = contour
        self.x,self.y,self.w,self.h = cv.boundingRect(contour)
        self.frame_count = 0
        self.max_frame = 8
        self.kf = None
        # self.centroid = (self.x+self.w)//2,(self.y+self.h)//2
        self.histogram = calculate_histogram(self.frame,self.contour)
        self.kf = KalmanFilter()
        
        

    
