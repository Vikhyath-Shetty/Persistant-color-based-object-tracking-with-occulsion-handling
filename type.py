from typing import List, Tuple
from numpy.typing import NDArray
import numpy as np

HSVBound = NDArray[np.uint8]
HSVPair = Tuple[HSVBound, HSVBound]
HSVRange = List[HSVPair]

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)