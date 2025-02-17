from .random_rows import random_rows
from .generate_test_data import generate_test_data
from Utility.utility import handle_args

args_dict = {
    "random_rows": random_rows,
    "generate_test_data": generate_test_data
}

if __name__ == "__main__": handle_args(args_dict, "RandomRows")