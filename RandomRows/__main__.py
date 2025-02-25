from .random_rows import random_rows_by_condition, random_rows_by_donor, threshold
from Utility.utility import handle_args

args_dict = {
    "random_rows_by_condition": random_rows_by_condition,
    "random_rows_by_donor": random_rows_by_donor,
    "threshold": threshold
}

if __name__ == "__main__": handle_args(args_dict, "RandomRows")