

class Descriptor():
    
    def __init__(self, at, id_str, id_decoder_fcn, data):
        day, ident_str, rep = id_decoder_fcn(id_str)
        self.day        = day
        self.ident_str  = ident_str
        self.ident      = at[ident_str]
        self.rep        = rep
        self.data       = data

    def get(self, col_name):
        return self.data[col_name]


def decoder_fnc(id_str):
    day         = int(id_str[1])
    ident_str   = id_str[3:-5]
    rep         = ord(id_str[-5]) - ord('A')
    return (day, ident_str, rep)

assoc_table = {
    "4RR": 0, "4RL": 1, "4R": 2, "4L": 3, 
    "3RR": 4, "3RL": 5, "3R": 6, "3L": 7,
    "2RR": 8, "2RL": 9, "2R": 10, "2L": 11,
    "1RR": 12, "1RL": 13, "1R": 14, "1L": 15,

    # ---- Ethans numbering
    "16": 0, "15": 1, "14": 2, "13": 3, 
    "12": 4, "11": 5, "10": 6, "9": 7,
    "8": 8, "7": 9, "6": 10, "5": 11,
    "4": 12, "3": 13, "2": 14, "1": 15,
}

sham_idxs = [0, 2, 4, 6, 8, 10, 12, 14]

