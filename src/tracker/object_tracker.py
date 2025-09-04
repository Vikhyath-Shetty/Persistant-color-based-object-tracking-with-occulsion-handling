from typing import List
import cv2 as cv
import logging
from tracker import DetectedObject
from utils import *
import numpy as np

class ObjectTracker:
    id_counter = 0
    def __init__(self, stream_src: str | int, color: set, n: int) -> None:
        self.stream_src = stream_src
        self.color = color
        self.n = n
        self.cap = cv.VideoCapture(stream_src)
        self.flag = None
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open the stream source")
        self.tracked_objects: List[DetectedObject] = []
        self.detected_objects: List[DetectedObject] = []

    def run(self) -> None:
        logging.info("Running Object tracker")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                logging.warning("Failed to read frame")
                continue
            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = get_mask(hsv_frame, self.color)
            contours = get_n_contours(mask.copy(), self.n)
            if len(contours) > 0:
                for con in contours:
                    self.flag = 0
                    object = DetectedObject(frame,con)
                    for obj in self.tracked_objects:
                        if obj.compare_histogram(object):
                            self.flag = 1
                            obj.frame_count = 0
                            obj.kf.correct(np.array([[object.cent_x],[object.cent_y]]))
                            cv.rectangle(frame,(object.x,object.y),(object.x+object.w,object.y+object.h),(0,255,0),2)
                        else:
                            
                           
