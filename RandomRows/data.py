from .Plate import Plate as P

condition_df_layout = [
    ("CD63_p30_TIGIT" , P.CD63, ["ICAM", "p30", "TIGIT" , "p30 + TIGIT" ]),
    ("CD63_p30_PD1"   , P.CD63, ["ICAM", "p30", "PD1"   , "p30 + PD1"   ]),
    ("CD63_p30_KLRG1" , P.CD63, ["ICAM", "p30", "KLRG1" , "p30 + KLRG1" ]),
    ("CD63_p30_2A"    , P.CD63, ["ICAM", "p30", "2A"    , "p30 + 2A"    ]),
    ("CD63_p30_LILRB1", P.CD63, ["ICAM", "p30", "LILRB1", "p30 + LILRB1"]),
    ("PFR_p30_TIGIT"  , P.PFR , ["ICAM", "p30", "TIGIT" , "p30 + TIGIT" ]),
    ("PFR_p30_PD1"    , P.PFR , ["ICAM", "p30", "PD1"   , "p30 + PD1"   ]),
    ("PFR_p30_KLRG1"  , P.PFR , ["ICAM", "p30", "KLRG1" , "p30 + KLRG1" ]),
    ("PFR_p30_2A"     , P.PFR , ["ICAM", "p30", "2A"    , "p30 + 2A"    ]),
    ("PFR_p30_LILRB1" , P.PFR , ["ICAM", "p30", "LILRB1", "p30 + LILRB1"]),
]