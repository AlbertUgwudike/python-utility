from .figures import figures
from Utility.utility import handle_args

args_dict = {
    "figures": figures
}

if __name__ == "__main__": handle_args(args_dict, "Figures")