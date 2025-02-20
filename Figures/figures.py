import numpy as np
import matplotlib.pyplot as plt

from typing import List
from .Desc import Desc

R = 512

# tigit_data = [
#     Desc("250116", "ICAM",               5, (1, 2, 3), (15, 30, 14)),
#     Desc("250214", "ICAM\+p30",         19, (1, 2, 3), (30, 30, 14)),
#     Desc("250206", "ICAM\+TIGIT",        2, (2, 0, 3), (30, 30, 14)),
#     Desc("250206", "ICAM\+p30\+TIGIT",   1, (2, 0, 3), (30, 30, 14)),
# ]

tigit_data = [
    Desc("250116", "ICAM",               4, (1, 2, 3), (15, 30, 14)),
    Desc("250214", "ICAM\+p30",          2, (1, 2, 3), (30, 30, 14)),
    Desc("250206", "ICAM\+TIGIT",        1, (2, 0, 3), (30, 30, 14)),
    Desc("250206", "ICAM\+p30\+TIGIT",   0, (2, 0, 3), (30, 30, 14)),
]

def figures():
    generate_figure(tigit_data)
    
    
def generate_figure(data: List[Desc]):   
    out = np.empty((512 * 4, 512 * 4, 3))
    for j in range(4):
        desc = data[j]
        img = desc.get_image()
        for i in range(3):
            thresh = desc.thresh[i] * 1000
            chn = img[i, :, :].clip(max = thresh) / thresh
            out[(R * j):(R * j + R), (R * i):(R * i + R), 2 - i] = chn
            out[(R * j):(R * j + R), (R * 3):(R * 3 + R), 2 - i] = chn

    plt.imshow(out)
    plt.imsave("./images/out.tiff", out)
    plt.show()
        




