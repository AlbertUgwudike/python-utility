import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import List, Tuple
from Figures.Desc import Desc, Channel as CH
from RandomRows.random_rows import organise_dfs, sort_tform
from RandomRows.data import condition_df_layout
from .data import donors
from Utility.utility import gauss, parfor, norm, unzip, fmap

IMG_SIZE = (512, 512)
XLS_DIR  = "./RandomRows/csv_example/"
CSV_DIR  = "./RandomRows/csv_out/"
OUT_DIR  = "./Regions/csv_out/"
ORG_DIR  = "./Regions/csv_org/"
CD63_COL = 10
PFR_COL  = 14
BG_ROW   = 2
THRESH_F = 100

def regions():
    start = time.time()
    parfor(process, donors)
    print(time.time() - start)

def visualise_distributions():
    res = parfor(calculate_dists, donors)
    _, axs = plt.subplots(len(res), 2)
    for i in range(len(res)):
        # (cd63_bg, cd63_sh, pfr_bg, pfr_sh)
        tings = ((res[i][0], res[i][1]), (res[i][2], res[i][3]))
        for j in range(2):
            (bg, sh) = tings[j]
            ax = axs[i][j]
            ax.hist(sh.flatten(), 100, range=(-100000, 500000), color='gray')
            ax.axvline(bg[0, :].mean(), color='r')
            ax.axvline(bg[0, :].mean() + 100 * bg[0, :].std(), color='g')
            if i < len(res) - 1: ax.get_xaxis().set_ticks([])

    plt.show()

def regions_by_condition():
    names   = [ fn.replace(".csv", "") for fn in os.listdir(OUT_DIR) ]
    csv_fns = [ f"{OUT_DIR}{fn}.csv" for fn in names ]
    csvs    = [ pd.read_csv(csv_fn) for csv_fn in csv_fns ]
    dfs     = ([ select_cols(df, "CD63") for df in csvs ], [ select_cols(df, "PFR") for df in csvs ])

    for (fn, idx, sheet_names) in condition_df_layout:
        df = organise_dfs(dfs[idx.value], names, sheet_names).sort_values('Name', key=sort_tform)
        df.to_csv(f"{ORG_DIR}{fn}.csv", index=False)

def select_cols(df: pd.DataFrame, marker: str) -> pd.DataFrame:
    parition = df[[col for col in df.columns if marker in col]]
    return parition.rename(columns = lambda c: c.replace(f"{marker} ", ""))

def process(args):
    (donor_id, shadow_data) = args
    (pfr_thresh, cd63_thresh) = [ get_empty_val_thresh(shadow_data, chn) for chn in [CH.PFR, CH.CD63] ]
    cd63_percs = calc_perc(donor_id, "CD63 ", *cd63_thresh)
    pfr_percs  = calc_perc(donor_id, "PFR ", *pfr_thresh)
    name_df = pd.DataFrame(data=[donor_id], columns=["Name"])
    df = pd.concat((name_df, cd63_percs, pfr_percs), axis=1)
    df.to_csv(f"{OUT_DIR}{donor_id}.csv")
    print("Processed", donor_id)

def calculate_dists(args) -> Tuple[np.ndarray, np.ndarray]:
    (donor_id, shadow_data) = args
    (pfr_empty_vals, cd63_empty_vals) = [ get_empty_val_thresh(shadow_data, chn) for chn in [CH.PFR, CH.CD63] ]
    cd63_bg, cd63_sh = calc_dists(donor_id, "CD63 ", *cd63_empty_vals)
    pfr_bg, pfr_sh  = calc_dists(donor_id, "PFR ", *pfr_empty_vals)
    return (cd63_bg, cd63_sh, pfr_bg, pfr_sh)

def get_empty_val_thresh(data: List[Tuple[Desc, List[int]]], chn: CH) -> Tuple[float, float]:
    # For clarity: returns empty vals for all (ICAM + other) in one array
    empty_vals = np.hstack([ compute_averages(*p, chn) for p in data ])
    return (empty_vals.mean(), empty_vals.std())

def get_empty_vals(data: List[Tuple[Desc, List[int]]], chn: CH) -> Tuple[float, float]:
    # For clarity: returns empty vals for all (ICAM + other) in one array
    return np.hstack([ compute_averages(*p, chn) for p in data ])

def compute_averages(des: Desc, img_ns: List[int], chn: CH) -> np.ndarray:
    data = [ (des.get_image(n), des.get_roi_mask(n, IMG_SIZE)) for n in img_ns ]
    return [ masked_average(*p, chn.value) for p in data ]
   
def masked_average(img: np.ndarray, mask: np.ndarray, channel: int) -> float:
    selection = img[channel, :, :][mask == 1]
    return selection.mean()

def get_background_mu(donor_id: str, sheet_name: str, bg_col: int) -> float:
    csv_fn = [ f"{XLS_DIR}{fn}" for fn in os.listdir(XLS_DIR) if donor_id in fn ][0]
    df = pd.read_excel(csv_fn, sheet_name)
    assert("Background" in df.columns[bg_col])
    return df.iloc[BG_ROW, bg_col]
    
def compute(donor_id: str, ext: str, empty_mu: float, empty_std: float):
    csv_fn   = [ f"{CSV_DIR}{fn}" for fn in os.listdir(CSV_DIR) if donor_id in fn ][0]
    donor_df = pd.read_csv(csv_fn)
    s_cols   = [ col for col in donor_df.columns if ext in col ]
    vals     = donor_df[s_cols].to_numpy()
    cols     = [ col.replace(ext, "") for col in s_cols ]
    bg_col   = CD63_COL if "CD63" in ext else PFR_COL

    # correct means for empty shadows by subtrating image specific background vals
    bg_mu = [ empty_mu - get_background_mu(donor_id, sn, bg_col) for sn in cols ]
    bg_mu = np.expand_dims(np.array(bg_mu), 0).repeat(vals.shape[0], 0)

    # background standard deviation is invariant to mean shift
    bg_std = empty_std * np.ones(bg_mu.shape)
    
    mu  = vals.mean(0, keepdims=True).repeat(vals.shape[0], 0)
    std = vals.std(0, keepdims=True).repeat(vals.shape[0], 0)

    return (mu, std, bg_mu, bg_std, vals, s_cols)

def calc_perc(donor_id: str, ext: str, empty_mu: float, empty_std: float) -> pd.DataFrame:
    (mu, std, bg_mu, bg_std, vals, s_cols) = compute(donor_id, ext, empty_mu, empty_std)
    gauss_diff = gauss(mu, std, vals) - gauss(bg_mu, bg_std, vals)
    mask       = gauss_diff > 4e-02
    percs      = 100 * mask.sum(0) / mask.shape[0]
    return pd.DataFrame(data=np.expand_dims(percs, 0), columns=s_cols)

def calc_dists(donor_id: str, ext: str, empty_mu: float, empty_std: float) -> pd.DataFrame:
    (mu, std, bg_mu, bg_std, vals, _) = compute(donor_id, ext, empty_mu, empty_std)
    return (bg_mu, vals)