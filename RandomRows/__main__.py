from .random_rows import random_rows
from Utility.utility import handle_args

args_dict = {
    "random_rows": random_rows
}

if __name__ == "__main__": handle_args(args_dict, "RandomRows")