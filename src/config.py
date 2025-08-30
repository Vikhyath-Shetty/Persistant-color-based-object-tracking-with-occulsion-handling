from typing import Dict
import numpy as np
from type import HSVRange

COLOR_RANGES: Dict[str, HSVRange] = {
    # ranges are in the order of low,high,low,high ....
    "red": [(np.array([20, 150, 100]), np.array([30, 255, 255])),
            (np.array([170, 100, 100]), np.array([179, 255, 255]))],
    "green": [(np.array([35, 50, 50]), np.array([85, 255, 255]))],
    "blue": [(np.array([94, 80, 2]), np.array([126, 255, 255]))],
    "yellow": [(np.array([15, 150, 150]), np.array([35, 255, 255]))]
}