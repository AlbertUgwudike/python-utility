import sys
import numpy as np
import operator
import re

from typing import List



from matplotlib.colors import ListedColormap
from functools import reduce

def handle_args(args_dict, module_name):
    if len(sys.argv) != 2 or sys.argv[1] not in args_dict.keys(): 
        print("Usage: ")
        for key in args_dict.keys(): print(f"python3 -m {module_name} {key}")
    else: args_dict[sys.argv[1]]()

def filter_nan(arr: np.ndarray): 
    return arr[np.logical_not(np.isnan(arr))]

def fmap(f, lst):
    return list(map(f, lst))

def vec_hcat(vecs):
    f = lambda v: np.expand_dims(v, 1)
    return np.hstack(fmap(f, vecs))

def concat(lst: List[List[str]]) -> List[str]:
    return reduce(operator.add, lst, [])

def zip_with(f, l1, l2): 
    return fmap(f, zip(l1, l2))

def issubset(s1, s2):
    return set(s1).issubset(set(s2))

def cmap(idx):
    N = 1024
    vals = np.zeros((N, 4))
    vals[:, 2 - idx] = np.linspace(0, 1, N)
    vals[:, 3] = 1
    return ListedColormap(vals)
