import cv2 as cv
import logging
from utils import *


class ObjectTracker:
    def __init__(self, stream_src: str | int, color: set, n: int) -> None:
        self.stream_src = stream_src
        self.color = color
        self.n = n
        self.cap = cv.VideoCapture(stream_src)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open the stream source")
        self.tracked_objects = []

    def run(self) -> None:
        logging.info("Running Object tracker")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                logging.warning("Failed to read frame")
                continue
            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = get_mask(hsv_frame, self.color)
            objects = get_n_objects(mask, self.n)
            for x,y,w,h in objects:
                cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                print((x,y,w,h))
            cv.imshow('Frame',frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break    
