from .rename import rename
from Utility.utility import handle_args

args_dict = {
    "rename": rename
}

if __name__ == "__main__": handle_args(args_dict, "Rename")