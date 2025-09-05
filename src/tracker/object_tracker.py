from typing import List
import cv2 as cv
import logging
from .detected_object import DetectedObject
from utils import *
import numpy as np

class ObjectTracker:
    def __init__(self, stream_src: str | int, color: set, n: int) -> None:
        self.color = color
        self.n = n
        self.id_counter = 0
        self.cap = cv.VideoCapture(stream_src)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open the stream source")
        self.tracked_objects: List[DetectedObject] = []

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
                    self.id_counter += 1
                    detected = DetectedObject(self.id_counter,frame,con)
                    matched = False
                    
                    for obj in self.tracked_objects:
                        if obj.compare_histogram(detected):
                            matched = True
                            obj.frame_count = 0
                            obj.kf.correct(np.array([[detected.cent_x],[detected.cent_y]],dtype=np.float32))
                            cv.rectangle(frame,(detected.x,detected.y),(detected.x+detected.w,detected.y+detected.h),(0,255,0),2)
                            break

                    if not matched:
                        self.tracked_objects.append(detected)    

            for obj in self.tracked_objects:
                if obj.frame_count>0:
                    obj.frame_count += 1
                    x, y, w, h = obj.kf.predict()
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) #type:ignore

            self.tracked_objects = [obj for obj in self.tracked_objects if obj.frame_count<=obj.max_frame_missed]
            cv.imshow('Object Tracking',frame)
            print(len(self.tracked_objects))
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv.destroyAllWindows()   

                            
                           
