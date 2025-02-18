import pandas as pd
import numpy as np
import os

from typing import List
from Utility.utility import filter_nan, fmap, zip_with

COL_CD63 = "Corrected CD63"
COL_PFR  = "Corrected PFR"
COL_REF  = "Background"
IN_DIR  = "./RandomRows/csv_example/"
OUT_DIR = "~/projects/python-utility/RandomRows/csv_out/"

def random_rows():
    content     = [ fn for fn in os.listdir(IN_DIR) if ".xlsx" in fn ]
    names       = [ fn.replace(".xlsx", "") for fn in content ]
    fns         = [ IN_DIR + n for n in content ]
    fn_sheets   = [ (fn, pd.ExcelFile(fn).sheet_names) for fn in fns ]
    dfs_cd63    = [ extract_rows(*p, COL_CD63) for p in fn_sheets ]
    dfs_pfr     = [ extract_rows(*p, COL_PFR) for p in fn_sheets ]
    dfs         = [ pd.concat(p, axis=1) for p in zip(dfs_cd63, dfs_pfr) ]

    for i, df in enumerate(dfs):
        df.to_csv(f"{OUT_DIR}{names[i]}.csv")

def extract_rows(xls_fn: str, sheet_names: List[str], col: str) -> pd.DataFrame:
    print(xls_fn, col)
    n_samples = least_count(xls_fn, len(sheet_names))
    dfs  = [ pd.read_excel(xls_fn, sn) for sn in sheet_names ]
    vecs = [ extract(df, n_samples, col) for df in dfs ]
    cols = [ f"{col} {sn}" for sn in sheet_names ]
    data = np.hstack(vecs)
    means = data.mean(0, keepdims=True)
    data_with_means = np.vstack([data, np.zeros(means.shape), means])
    return pd.DataFrame(data=data_with_means, columns=cols)

def extract(df: pd.DataFrame, n_samples: int, col: str) -> np.ndarray:
    out = n_random_rows(read_col(df, col), n_samples)
    return np.expand_dims(out, 1)

def n_random_rows(arr: np.ndarray, n_samples: int) -> np.ndarray:
    arr_cp = arr.copy()
    np.random.shuffle(arr_cp)
    return arr_cp[:n_samples]

def calculate_n(df: pd.DataFrame):
    return read_col(df, COL_REF).size

def least_count(xls_fn, n_sheets):
    f = lambda n: calculate_n(pd.read_excel(xls_fn, n))
    return min(map(f, range(n_sheets)))

def read_col(df: pd.DataFrame, col_name: str) -> np.ndarray:
    return filter_nan(df[col_name].to_numpy())





