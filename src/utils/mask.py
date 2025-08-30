import cv2 as cv
from cv2.typing import MatLike
from config import COLOR_RANGES
import numpy as np


def get_red_mask(frame: MatLike) -> MatLike:
    red_range = COLOR_RANGES["red"]
    lower_range_mask = cv.inRange(frame, red_range[0][0], red_range[0][1])
    upper_range_mask = cv.inRange(frame, red_range[1][0], red_range[1][1])
    return cv.bitwise_or(lower_range_mask, upper_range_mask)


def get_other_mask(frame: MatLike, color: str) -> MatLike:
    color_range = COLOR_RANGES[color]
    return cv.inRange(frame, color_range[0][0], color_range[0][1])


def get_mask(frame: MatLike, color: set) -> MatLike:
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    for col in color:
        if col == "red":
            temp = get_red_mask(frame)
        else:
            temp = get_other_mask(frame, col)
        mask = cv.bitwise_or(temp, mask)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    return mask
