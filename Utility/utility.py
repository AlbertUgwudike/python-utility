import sys
import numpy as np
import operator

from multiprocessing import Pool
from typing import List, TypeVar, Tuple
from matplotlib.colors import ListedColormap
from functools import reduce
from itertools import groupby

T = TypeVar("T")
U = TypeVar("U")

def handle_args(args_dict, module_name):
    if len(sys.argv) != 2 or sys.argv[1] not in args_dict.keys(): 
        print("Usage: ")
        for key in args_dict.keys(): print(f"python3 -m {module_name} {key}")
    else: args_dict[sys.argv[1]]()

def filter_nan(arr: np.ndarray): 
    return arr[np.logical_not(np.isnan(arr))]

def fmap(f, lst):
    return list(map(f, lst))

def filt(f, lst):
    return list(filter(f, lst))

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

def gauss(mu: float, std: float, x: np.ndarray) -> np.ndarray:
    factor = (1 / ((2 * np.pi * (std ** 2)))) ** 0.5
    exp = ((x - mu) ** 2) / (-2 * std ** 2)
    return factor * np.e ** exp

def norm(mu: float, std: float, x: np.ndarray) -> np.ndarray:
    return (x - mu) / std

def parfor(f, args):
    res = []
    with Pool() as pool: 
        res = pool.map(f, args)
    return res

def fst(tup: Tuple[T, U]) -> T:
    return tup[0]

def snd(tup: Tuple[T, U]) -> U:
    return tup[1]

def unzip(l): return list(zip(*l))

def group_by(f, lst):
    return fmap(lambda g: list(snd(g)), groupby(lst, key=f))

def pad(lst, l, v):
    return (lst + [v] * l)[:l]

def flatten(lst):
    return [x for xs in lst for x in xs]
