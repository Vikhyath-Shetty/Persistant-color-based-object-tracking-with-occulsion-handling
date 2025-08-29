from typing import Sequence, List
import logging
import cv2 as cv
from config import COLOR_RANGES
from cv2.typing import MatLike, Rect
import numpy as np
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")


def create_other_mask(frame: MatLike, color: str) -> MatLike:
    color_range = COLOR_RANGES[color]
    return cv.inRange(frame, color_range[0][0], color_range[0][1])


def create_red_mask(frame: MatLike) -> MatLike:
    red_range = COLOR_RANGES["red"]
    lower_mask = cv.inRange(frame, red_range[0][0], red_range[0][1])
    upper_mask = cv.inRange(frame, red_range[1][0], red_range[1][1])
    mask = cv.bitwise_or(lower_mask, upper_mask)
    return mask


def create_mask(frame: MatLike, color: set) -> MatLike | None:
    mask = None
    for col in color:
        if col == "red":
            temp_mask = create_red_mask(frame)
        else:
            temp_mask = create_other_mask(frame, col)
        mask = temp_mask if mask is None else cv.bitwise_or(temp_mask, mask)
    return mask


def get_contours(mask: MatLike) -> MatLike:
    kernal = np.ones((5, 5), np.uint8)
    morphed_mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernal)
    contours, _ = cv.findContours(
        morphed_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    return contours


def get_contour_cordinates(contours: MatLike, n: int) -> List[tuple]:
    coordinates = []
    selected_contours = sorted(
        contours, key=cv.contourArea, reverse=True)[:min(n, len(contours))]
    for con in selected_contours:
        cord = cv.boundingRect(con)
        coordinates.append(cord)
    return coordinates


def predict_position(frame: MatLike, coordinates: List[tuple]) -> None:
    pass


def detect_position(frame: MatLike, contours: MatLike, n: int) -> None:
    coordinates = get_contour_cordinates(contours, n)
    for cord in coordinates:
        x, y, w, h = cord
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


def init_kalman() -> None:
    kf = cv.KalmanFilter(4, 2)
    kf.transitionMatrix = np.array([
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    kf.measurementMatrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ])
    kf.processNoiseCov = np.eye(4)*0.01
    kf.measurementNoiseCov = np.eye(2)*0.01


def detect_object(cam_src: str | int, color: set, n: int) -> None:
    cap = cv.VideoCapture(cam_src)
    if not cap.isOpened():
        raise RuntimeError("Failed to open the camera source")
    try:
        # init_kalman()
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.warning("Failed to read the frame from the stream")
                continue
            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = create_mask(hsv_frame, color)
            if mask is None:
                logging.warning("Failed to create mask")
                continue
            contours = get_contours(mask)
            if contours:
                detect_position(frame, contours, n)
            cv.imshow("Object Detection", frame)    
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv.destroyAllWindows()
