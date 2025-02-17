import sys
import numpy as np
import operator
from typing import List

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