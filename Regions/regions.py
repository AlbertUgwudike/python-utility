import os
import numpy as np
import pandas as pd

from typing import List, Tuple
from Figures.Desc import Desc, Channel as CH
from .data import donors

IMG_SIZE = (512, 512)
XLS_DIR  = "./RandomRows/csv_example/"
CSV_DIR  = "./RandomRows/csv_out/"
OUT_DIR  = "./Regions/csv_out/"
CD63_COL = 10
PFR_COL  = 14
BG_ROW   = 2

def regions():
    for (d_id, donor) in donors:
        print("Processing", d_id)
        df = process(d_id, donor)
        df.to_csv(f"{OUT_DIR}{d_id}.csv")

def process(donor_id: str, shadow_data) -> pd.DataFrame:
    empty_vals = [ get_empty_vals(shadow_data, chn).mean() for chn in [CH.PFR, CH.CD63] ]
    cd63_percs = calc_perc(donor_id, "CD63 ", empty_vals[1])
    pfr_percs  = calc_perc(donor_id, "PFR ", empty_vals[0])
    name_df = pd.DataFrame(data=[donor_id], columns=["Name"])
    return pd.concat((name_df, cd63_percs, pfr_percs), axis=1)

def get_empty_vals(data: List[Tuple[Desc, List[int]]], chn: CH) -> np.ndarray:
    return np.hstack([ compute_averages(*p, chn) for p in data ])

def compute_averages(des: Desc, img_ns: List[int], chn: CH) -> np.ndarray:
    data = [ (des.get_image(n), des.get_roi_mask(n, IMG_SIZE)) for n in img_ns ]
    return [ masked_average(*p, chn.value) for p in data ]
   
def masked_average(img: np.ndarray, mask: np.ndarray, channel: int) -> float:
    selection = img[channel, :, :][mask == 1]
    return selection.mean()

def get_background_val(donor_id: str, sheet_name: str, bg_col: int) -> float:
    csv_fn = [ f"{XLS_DIR}{fn}" for fn in os.listdir(XLS_DIR) if donor_id in fn ][0]
    df = pd.read_excel(csv_fn, sheet_name)
    assert("Background" in df.columns[bg_col])
    return df.iloc[BG_ROW, bg_col]

    
def calc_perc(donor_id: str, ext: str, empty_val: float) -> np.ndarray:
    csv_fn   = [ f"{CSV_DIR}{fn}" for fn in os.listdir(CSV_DIR) if donor_id in fn ][0]
    donor_df = pd.read_csv(csv_fn)
    s_cols   = [ col for col in donor_df.columns if ext in col ]
    cols     = [ col.replace(ext, "") for col in s_cols ]
    bg_col   = CD63_COL if "CD63" in ext else PFR_COL
    bg_vals  = np.array([ empty_val - get_background_val(donor_id, sn, bg_col) for sn in cols ])
    vals     = donor_df[s_cols].to_numpy()[:-2, :]
    mask     = vals > np.expand_dims(bg_vals, 0).repeat(vals.shape[0], 0)
    percs    = 100 * mask.sum(0) / mask.shape[0]
    return pd.DataFrame(data=np.expand_dims(percs, 0), columns=s_cols)