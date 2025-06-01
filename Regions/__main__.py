from .regions import regions, regions_by_condition, visualise_distributions
from Utility.utility import handle_args

args_dict = {
    "regions": regions,
    "regions_by_condition": regions_by_condition,
    "visualise_distributions": visualise_distributions
}

if __name__ == "__main__": handle_args(args_dict, "Regions")