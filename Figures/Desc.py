import nd2
import os
import numpy as np

from typing import Tuple, List
from enum import Enum
from roifile import roiread, ImagejRoi
from PIL import Image, ImageDraw

INPUT_PATH = "./data/shadows/"
ROI_BG_NAME = "ROI_BG/"

class Condition(Enum):
    ICAM    = 0
    NKP30   = 1
    NKG2A   = 2
    TIGIT   = 3
    LILRB   = 4
    KLR2G   = 5
    PD1     = 6

    def to_str(self) -> str:
        strs = ["ICAM", "p30", "2A", "TIGIT", "LILRB", "KLRG", "PD1"]
        return strs[self.value]
    
class Desc:
    def __init__(
            self, 
            donor_id: str, 
            condition_id: List[Condition],
            order: Tuple[int, int, int]
        ):

        self.donor_id = donor_id
        self.condition_id = condition_id
        self.order = order

    def get_image(d, img_n) -> np.ndarray:
        img_fn = d.get_image_fn()
        return nd2.imread(img_fn)[img_n, d.order, :, :]
    
    def get_image_fn(d) -> str:
        folder_name = d.get_folder_name()
        img_fns = [ f"{folder_name}/{fn}" for fn in os.listdir(folder_name) if d.matches_fn(fn) ]
        assert(len(img_fns) == 1)
        return img_fns[0]
    
    def get_folder_name(d) -> str:
        folder_names = [ INPUT_PATH + fn for fn in os.listdir(INPUT_PATH) if d.donor_id in fn ]
        assert(len(folder_names) == 1)
        return folder_names[0]
    
    def matches_fn(d, fn) -> bool:
        negatives = [c for c in Condition if c not in d.condition_id]
        present = all(c.to_str() in fn for c in d.condition_id)
        absent  = all(c.to_str() not in fn for c in negatives)
        return present and absent
    
    def get_roi(d, img_n: int, sz: Tuple[int, int]) -> np.ndarray:
        folder_path = f"{d.get_folder_name()}/{ROI_BG_NAME}"
        roi_fps = [folder_path + fn for fn in os.listdir(folder_path) if d.matches_fn(fn)]
        roi_fns = [f"{roi_fps[0]}/{fnn}" for fnn in os.listdir(roi_fps[0]) ]
        rois = [ roiread(fnn) for fnn in roi_fns]
        roi = next(filter(lambda roi: roi.t_position == img_n + 1, rois))
        coords = [tuple(p) for p in roi.coordinates()]
        img = Image.new('L', sz, 0)
        ImageDraw.Draw(img).polygon(coords, outline=1, fill=1)
        return np.array(img)
        
class Channel(Enum):
    ICAM = 0
    CD63 = 1
    PFR  = 2
    


