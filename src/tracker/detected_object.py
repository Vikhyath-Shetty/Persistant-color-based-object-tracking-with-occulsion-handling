import cv2 as cv
from cv2.typing import MatLike
from utils import calculate_histogram
import matplotlib.pyplot as plt

class DetectedObject:
    def __init__(self, frame: MatLike, mask: MatLike, object: tuple) -> None:
        self.x, self.y, self.w, self.h = object
        self.centroid = ((self.x+self.w)//2, ((self.y+self.h)//2))
        self.roi_mask = mask[self.y:self.y+self.h,self.x:self.x+self.w]
        self.roi_frame = frame[self.y:self.y+self.h, self.x:self.x+self.w]
        self.histogram = calculate_histogram(self.roi_frame,self.roi_mask)
        # kalman = get_kalman_filter(self.centroid)

    
