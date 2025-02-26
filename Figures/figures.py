import numpy as np

from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as I
from typing import List, Tuple
from .Desc import Desc
from .descriptor_sets import tigit_data, klrg_data, pd1_data, lilrb_data

D  = 150
R  = 75
S  = D + 3
BY = 140
BH = 2
BX = 110
BW = 33 # 5microns

def figures():
    generate_figure(tigit_data, "tigit")
    generate_figure(klrg_data, "klrg")
    generate_figure(pd1_data, "pd1")
    generate_figure(lilrb_data, "lirb")
    
def generate_figure(data: List[Tuple[Desc, int, Tuple[int, int, int], Tuple[int, int]]], out_fn: str):   
    out = -np.ones((S * 4, S * 4, 3))
    for j in range(4):
        desc, img_n, thresh, (r, c) = data[j]
        img = desc.get_image(img_n)
        for i in range(3):
            t = thresh[i] * 1000
            chn = img[i, (r - R):(r + R), (c - R):(c + R)].clip(min = 0, max = t) / t
            out[(S * j):(S * j + D), (S * i):(S * i + D), 2 - i] = chn
            out[(S * j):(S * j + D), (S * 3):(S * 3 + D), 2 - i] = chn
            out[(S * j + BY):(S * j + BY + BH), (S * i + BX):(S * i + BX + BW), :] = 1
        
        out[(S * j + BY):(S * j + BY + BH), (S * 3 + BX):(S * 3 + BX + BW), :] = 1

    out = set_bg(out, -1)
    img = label_scale_bar(np.uint8(out * 255), "5µm")
    img.save(f"./data/images/{out_fn}.tiff")
    print(out_fn + " done!")
        
def set_bg(arr, bg_marker):
    bg = np.all((arr == bg_marker), axis=2)
    bg = np.expand_dims(bg, 2).repeat(3, 2)
    arr[bg] = 1
    arr[arr == bg_marker] = 0
    return arr

def label_scale_bar(arr: np.ndarray, txt: str) -> I:
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./data/assets/font.ttf", 16)
    draw.text((570, 580), txt, (255, 255, 255), font=font)
    return img


