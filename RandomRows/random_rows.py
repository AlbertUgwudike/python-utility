import pandas as pd
import numpy as np
import os

from typing import List, Tuple
from Utility.utility import filter_nan, issubset
from .Plate import Plate as P
from .data import condition_df_layout

COL_CD63 = "Corrected CD63"
COL_PFR  = "Corrected PFR"
COL_REF  = "Background"
IN_DIR   = "./RandomRows/csv_example/"
OUT_DIR  = "~/projects/python-utility/RandomRows/csv_out/"
OUT_DIR_T  = "~/projects/python-utility/RandomRows/csv_out_t/"

def random_rows_by_condition():
    names, dfs = random_rows()
    for (fn, idx, sheet_names) in condition_df_layout:
        df = organise_dfs(dfs[idx.value], names, sheet_names).sort_values('Name', key=sort_tform)
        df.to_csv(f"{OUT_DIR}{fn}.csv", index=False)

def random_rows_by_donor():
    names, dfs_p = random_rows()
    dfs = [ pd.concat(p, axis=1) for p in zip(dfs_p) ]

    for i, df in enumerate(dfs):
        data = df.iloc[:, :].to_numpy()
        means = data.mean(0)
        data_means = np.vstack((data, np.zeros(means.shape), means))
        n_cols = len(df.columns) // 2
        cd63_cols = [ "CD63 " + n for n in df.columns[:n_cols] ]
        pfr_cols  = [ "PFR "  + n for n in df.columns[n_cols:] ]
        out_df = pd.DataFrame(data=data_means, columns=cd63_cols + pfr_cols)
        out_df.to_csv(f"{OUT_DIR}{names[i]}.csv")


def random_rows() -> Tuple[List[str], Tuple[List[pd.DataFrame], List[pd.DataFrame]]]:
    content     = [ fn for fn in os.listdir(IN_DIR) if ".xlsx" in fn ]
    names       = [ fn.replace(".xlsx", "") for fn in content ]
    fns         = [ IN_DIR + n for n in content ]
    fn_sheets   = [ (fn, pd.ExcelFile(fn).sheet_names) for fn in fns ]
    dfs_cd63    = [ extract_rows(*p, COL_CD63) for p in fn_sheets ]
    dfs_pfr     = [ extract_rows(*p, COL_PFR) for p in fn_sheets ]
    return (names, (dfs_cd63, dfs_pfr))

def organise_dfs(dfs: List[pd.DataFrame], replicate_names: List[str], sheet_names: List[str]) -> pd.DataFrame:
    dfs1 = [ (df, rn) for (df, rn) in zip(dfs, replicate_names) if issubset(sheet_names, df.columns)]
    dfs2 = [ (df[sheet_names], rn) for (df, rn) in dfs1 ]
    f = lambda p: (pd.DataFrame(np.repeat(p[1], len(p[0])), columns=["Name"]), p[0])
    dfs3 = [ pd.concat(f(p), axis=1) for p in dfs2 ]
    return pd.concat(dfs3, axis=0)

def extract_rows(xls_fn: str, sheet_names: List[str], col: str) -> pd.DataFrame:
    print(xls_fn, col)
    n_samples = least_count(xls_fn, len(sheet_names))
    dfs  = [ pd.read_excel(xls_fn, sn) for sn in sheet_names ]
    vecs = [ extract(df, n_samples, col) for df in dfs ]
    data = np.hstack(vecs)
    return pd.DataFrame(data=data, columns=sheet_names, index=None)

def extract(df: pd.DataFrame, n_samples: int, col: str) -> np.ndarray:
    out = n_random_rows(read_col(df, col), n_samples)
    return np.expand_dims(out, 1)

def n_random_rows(arr: np.ndarray, n_samples: int) -> np.ndarray:
    arr_cp = arr.copy()
    np.random.seed(42)
    np.random.shuffle(arr_cp)
    return arr_cp[:n_samples]

def calculate_n(df: pd.DataFrame):
    return read_col(df, COL_REF).size

def least_count(xls_fn, n_sheets):
    f = lambda n: calculate_n(pd.read_excel(xls_fn, n))
    return min(map(f, range(n_sheets)))

def read_col(df: pd.DataFrame, col_name: str) -> np.ndarray:
    return filter_nan(df[col_name].to_numpy())

def sort_tform(col: pd.Series) -> pd.Series:
    tmp1 = col.map(lambda e: e[3:])
    tmp2 = tmp1.map(lambda e: e if e[0] == '2' else e[4:] + e[2:4] + e[:2])
    return tmp2
