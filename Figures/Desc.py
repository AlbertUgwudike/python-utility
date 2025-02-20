import nd2
import os
import numpy as np

from typing import Tuple
from Utility.utility import exact_in

INPUT_PATH = "/Volumes/Khodor-external-003/Vanessa_MRes/"

class Desc:
    def __init__(
            self, 
            replicate_id: str, 
            condition_id: str, 
            img_n: int, 
            order: Tuple[int, int, int],
            thresh: Tuple[int, int, int]
        ):

        self.replicate_id = replicate_id
        self.condition_id = condition_id
        self.img_n = img_n
        self.order = order
        self.thresh = thresh

    def get_image(d) -> np.ndarray:
        folder_name = [ INPUT_PATH + fn for fn in os.listdir(INPUT_PATH) if d.replicate_id in fn ][0]
        img_fn = [ f"{folder_name}/{fn}" for fn in os.listdir(folder_name) if exact_in(d.condition_id, fn) ][0]
        return nd2.imread(img_fn)[d.img_n, d.order, :, :]