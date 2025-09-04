from ast import List
import cv2 as cv
import logging
from tracker.detected_object import DetectedObject
from utils import *
from utils.contour import get_n_contours


class ObjectTracker:
    def __init__(self, stream_src: str | int, color: set, n: int) -> None:
        self.stream_src = stream_src
        self.color = color
        self.n = n
        self.cap = cv.VideoCapture(stream_src)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open the stream source")
        self.tracked_objects:list = []

    def run(self) -> None:
        logging.info("Running Object tracker")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                logging.warning("Failed to read frame")
                continue
            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = get_mask(hsv_frame, self.color)
            contours = get_n_contours(mask.copy(),self.n)
            if len(contours)>0:
                for con in contours:
                    obj = DetectedObject(frame, con)
                    print(obj.kf)
            
            
