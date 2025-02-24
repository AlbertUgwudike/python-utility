import numpy as np
import matplotlib.pyplot as plt

from Figures.Desc import Desc
from Figures.Desc import Condition as C
from Figures.Desc import Channel as CH

bg_selection = [
    (Desc("250206", [C.ICAM],        (2, 0, 3)), [5, 7, 9, 11]),
    (Desc("250206", [C.ICAM, C.PD1], (2, 0, 3)), [8, 11, 28]  ),
]

bg_statistics = {
    "250206": (
        [ 390.906, 379.735, 391.111, 380.052 ],
        [ 2306.926, 1826.498 ]
    )
}

def regions():
    des, img_ns = bg_selection[0]
    data = [(des.get_image(n), des.get_roi(n, (512, 512))) for n in img_ns]
    print(len(data))
    
    results = [average_intensity(*p, CH.CD63.value) for p in data]
    print(results)

    # plt.imshow(data[0][1])
    # plt.show()

def average_intensity(img: np.ndarray, mask: np.ndarray, channel: int) -> float:
    selection = img[channel, :, :][mask == 1]
    return selection.mean()
