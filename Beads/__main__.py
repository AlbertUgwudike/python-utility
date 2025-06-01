from Utility.utility import handle_args
from .organise import organise

args_dict = {
    "organise": organise
}

if __name__ == "__main__": handle_args(args_dict, "Beads")