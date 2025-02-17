import pandas as pd
import numpy as np

from typing import List
from Utility.utility import filter_nan, fmap, vec_hcat, concat

COL_CD63 = "Corrected CD63"
COL_PFR  = "Corrected PFR"
COL_REF  = "Background"
EXAMPLE_DIR = "~/projects/python-utility/RandomRows/csv_example/"
EXAMPLE_FNS = [ "D1_150125", "D1_250206", "D2_160125" ]
OUT_DIR = "~/projects/python-utility/RandomRows/csv_out/"

fns = fmap(lambda fn: EXAMPLE_DIR + fn + ".xlsx", EXAMPLE_FNS)

def random_rows():
    fn_and_sheets = fmap(lambda fn: (fn, pd.ExcelFile(fn).sheet_names), fns)
    dfs = map(lambda p: extract_rows(*p), fn_and_sheets)
    for i, df in enumerate(dfs):
        df.to_csv(f"{OUT_DIR}{EXAMPLE_FNS[i]}.csv")

def extract_rows(xls_fn: str, sheet_names: List[str]) -> pd.DataFrame:
    n_samples = least_count(xls_fn, len(sheet_names))
    generate_col_names = lambda sn: [f"{COL_CD63} {sn}", f"{COL_PFR} {sn}"]
    process = lambda sn: extract(pd.read_excel(xls_fn, sn), n_samples)
    data = np.hstack(fmap(process, sheet_names))
    col_names = concat(fmap(generate_col_names, sheet_names))
    return pd.DataFrame(data=data, columns=col_names)

def extract(df: pd.DataFrame, n_samples: int) -> np.ndarray:
    data_cd63 = n_random_rows(read_col(df, COL_CD63), n_samples)
    data_pfr = n_random_rows(read_col(df, COL_PFR), n_samples)
    return vec_hcat([data_cd63, data_pfr])

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





