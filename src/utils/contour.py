from typing import List, Tuple,Sequence
import cv2 as cv
from cv2.typing import MatLike


def get_n_contours(mask: MatLike, n: int) -> Sequence[MatLike]:
    contour, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contour, key=cv.contourArea, reverse=True)[
        :min(n, len(contour))]
    return sorted_contours


def get_n_coordinates(mask: MatLike, n: int) -> List[Tuple[int,int,int,int]]:
    coordinates = []
    contours = get_n_contours(mask,n)
    for con in contours:
        x,y,w,h = cv.boundingRect(con)
        coordinates.append((x,y,w,h))
    return coordinates    


