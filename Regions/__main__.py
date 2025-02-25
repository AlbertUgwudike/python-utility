from .regions import regions, regions_by_condition
from Utility.utility import handle_args

args_dict = {
    "regions": regions,
    "regions_by_condition": regions_by_condition
}

if __name__ == "__main__": handle_args(args_dict, "Regions")