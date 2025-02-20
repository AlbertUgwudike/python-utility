import pandas as pd
import numpy as np
import os

from typing import List
from Utility.utility import filter_nan, issubset

COL_CD63 = "Corrected CD63"
COL_PFR  = "Corrected PFR"
COL_REF  = "Background"
IN_DIR   = "./RandomRows/csv_example/"
OUT_DIR  = "~/projects/python-utility/RandomRows/csv_out/"

def random_rows():
    content     = [ fn for fn in os.listdir(IN_DIR) if ".xlsx" in fn ]
    names       = [ fn.replace(".xlsx", "") for fn in content ]
    fns         = [ IN_DIR + n for n in content ]
    fn_sheets   = [ (fn, pd.ExcelFile(fn).sheet_names) for fn in fns ]
    dfs_cd63    = [ extract_rows(*p, COL_CD63) for p in fn_sheets ]
    dfs_pfr     = [ extract_rows(*p, COL_PFR) for p in fn_sheets ]
    dfs         = [ pd.concat(p, axis=1) for p in zip(dfs_cd63, dfs_pfr) ]

    settings = [
        ("CD63_p30_TIGIT" , dfs_cd63, ["ICAM", "p30", "TIGIT" , "p30 + TIGIT" ]),
        ("CD63_p30_PD1"   , dfs_cd63, ["ICAM", "p30", "PD1"   , "p30 + PD1"   ]),
        ("CD63_p30_KLRG1" , dfs_cd63, ["ICAM", "p30", "KLRG1" , "p30 + KLRG1" ]),
        ("CD63_p30_2A"    , dfs_cd63, ["ICAM", "p30", "2A"    , "p30 + 2A"    ]),
        ("CD63_p30_LILRB1", dfs_cd63, ["ICAM", "p30", "LILRB1", "p30 + LILRB1"]),
        ("PFR_p30_TIGIT"  , dfs_pfr , ["ICAM", "p30", "TIGIT" , "p30 + TIGIT" ]),
        ("PFR_p30_PD1"    , dfs_pfr , ["ICAM", "p30", "PD1"   , "p30 + PD1"   ]),
        ("PFR_p30_KLRG1"  , dfs_pfr , ["ICAM", "p30", "KLRG1" , "p30 + KLRG1" ]),
        ("PFR_p30_2A"     , dfs_pfr , ["ICAM", "p30", "2A"    , "p30 + 2A"    ]),
        ("PFR_p30_LILRB1" , dfs_pfr , ["ICAM", "p30", "LILRB1", "p30 + LILRB1"]),
    ]
    
    for i, df in enumerate(dfs):
        df.to_csv(f"{OUT_DIR}{names[i]}.csv")

    for (fn, data, sheet_names) in settings:
        df = organise_dfs(data, names, sheet_names)
        df.to_csv(f"{OUT_DIR}{fn}.csv", index=False)

def organise_dfs(dfs: List[pd.DataFrame], replicate_names: List[str], sheet_names: List[str]) -> pd.DataFrame:
    dfs1 = [ df for df in dfs if issubset(sheet_names, df.columns)]
    dfs2 = [ df[sheet_names] for df in dfs1 ]
    f = lambda p: (pd.DataFrame(np.repeat(p[1], len(p[0])), columns=["Name"]), p[0])
    dfs3 = [ pd.concat(f(p), axis=1) for p in zip(dfs2, replicate_names) ]
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


