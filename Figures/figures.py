import numpy as np
import matplotlib.pyplot as plt

from typing import List
from .Desc import Desc
from .descriptor_sets import tigit_data, klrg_data, pd1_data, lilrb_data

R = 512
S = R + 3
UM_PER_PX = 0.16
BY = 450
BH = 25
BX = 325
BW = 133 # 20microns

def figures():
    generate_figure(tigit_data, "tigit")
    generate_figure(klrg_data, "klrg")
    generate_figure(pd1_data, "pd1")
    generate_figure(lilrb_data, "lirb")
    
def generate_figure(data: List[Desc], out_fn: str):   
    out = -np.ones((S * 4, S * 4, 3))
    for j in range(4):
        desc = data[j]
        img = desc.get_image()
        for i in range(3):
            thresh = desc.thresh[i] * 1000
            chn = img[i, :, :].clip(max = thresh) / thresh
            out[(S * j):(S * j + R), (S * i):(S * i + R), 2 - i] = chn
            out[(S * j):(S * j + R), (S * 3):(S * 3 + R), 2 - i] = chn
    
    out[(S * 0 + BY):(S * 0 + BY + BH), (S * 0 + BX):(S * 0 + BX + BW), :] = 0.75
    plt.imsave(f"./images/{out_fn}.tiff", set_bg(out, -1))
        
def set_bg(arr, bg_marker):
    bg = np.all((arr == bg_marker), axis=2)
    bg = np.expand_dims(bg, 2).repeat(3, 2)
    arr[bg] = 0.75
    arr[arr == bg_marker] = 0
    return arr


