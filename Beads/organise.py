import pandas as pd
import numpy as np

from Utility.utility import fmap, filt, group_by, pad, zip_with
from .Descriptor import Descriptor, assoc_table, decoder_fnc, sham_idxs

INPUT_FN        = "./data/facs/beeds.xlsx"
OUTPUT_FN       = "./Beads/csv_out/out.csv"
SHEET_NAME      = "predicted_conc"
ID_COL          = 1
DATA_START_COL  = 6
STD_END_ROW     = 16

def organise():
    input_df = pd.read_excel(INPUT_FN, SHEET_NAME)
    id_df    = input_df.iloc[:, ID_COL]
    data_df  = input_df.iloc[:, DATA_START_COL:]
    df       = pd.concat((id_df, data_df), axis=1)
    df       = df.iloc[STD_END_ROW:, :]

    row_fnc   = lambda i: Descriptor(assoc_table, df.iloc[i, 0], decoder_fnc, df.iloc[i, 1:])

    descs = fmap(row_fnc, range(len(df)))
    descs.sort(key = lambda d: d.ident)

    sham_descs = filt(lambda d: d.ident in sham_idxs, descs)
    fus_descs  = filt(lambda d: d.ident not in sham_idxs, descs)

    cyto_strs = ["IL-23 (A4)", "IL-1α (A5)", "IFN-γ (A6)", "IL-17A (B6)"]

    sham_data = fmap(lambda cs: process(sham_descs, cs), cyto_strs)
    fus_data  = fmap(lambda cs: process(fus_descs, cs), cyto_strs)

    data = zip_with(lambda p: pd.concat(p, axis=1), sham_data, fus_data)
    data = pd.concat(data, axis=0)

    print(data)

    data.to_csv(OUTPUT_FN)

def process(descs, cyto_str):
    g_descs  = group_by(lambda d: d.ident, descs)
    data     = fmap(lambda g: create_table(g, cyto_str), g_descs)

    idx    = fmap(lambda suf: f"{cyto_str}_D{suf}", [8, 1])
    idx_df = pd.DataFrame(data=idx, columns=["Day"])

    return pd.concat([idx_df] + data, axis=1)


def create_table(g, cyto_str):
    extract = lambda d: d.get(cyto_str)

    d8   = fmap(extract, filt(lambda d: d.day == 8, g))
    d1   = fmap(extract, filt(lambda d: d.day == 1, g))

    data      =  np.array([pad(d8, 2, "Nan"), pad(d1, 2, "Nan")], dtype=np.float32)
    data_cols = fmap(lambda suf: f"{g[0].ident_str}_REP{suf}", [1, 2])

    return pd.DataFrame(data=data, columns=data_cols)

