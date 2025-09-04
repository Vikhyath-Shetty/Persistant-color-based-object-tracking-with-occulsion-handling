import numpy as np
import cv2 as cv


class KalmanFilter:
    def __init__(self) -> None:
        self.kf = cv.KalmanFilter(4, 2)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0],
                                             [0, 1, 0, 1],
                                             [0, 0, 1, 0],
                                             [0, 0, 0, 1]], np.float32)

        self.kf.measurementMatrix = np.array([[1, 0, 0, 0],
                                              [0, 1, 0, 0]], np.float32)

        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.5


    def predict(self) -> tuple:
        prediction = self.kf.predict()
        center_x, center_y = int(prediction[0]), int(prediction[1])
        x, y = int(center_x - 60/2), int(center_y-40/2)
        w, h = int(center_x+60/2), int(center_y+40/2)
        return x, y, w, h

    def correct(self, measurement: np.ndarray) -> None:
        self.kf.correct(measurement)
