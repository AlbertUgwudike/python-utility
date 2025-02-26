from .random_rows import random_rows_by_condition, random_rows_by_donor, averages_per_donor
from Utility.utility import handle_args

args_dict = {
    "random_rows_by_condition": random_rows_by_condition,
    "random_rows_by_donor": random_rows_by_donor,
    "averages_per_donor": averages_per_donor
}

if __name__ == "__main__": handle_args(args_dict, "RandomRows")