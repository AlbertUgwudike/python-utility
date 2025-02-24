from .regions import regions
from Utility.utility import handle_args

args_dict = {
    "regions": regions
}

if __name__ == "__main__": handle_args(args_dict, "Regions")