import subprocess
import os
import re


IN_DIR  = "./RandomRows/csv_example/"

def rename():
    pattern = r"^.+(D\d) - (\d{6})"
    names   = [ name for name in os.listdir(IN_DIR) if ".xlsx" in name ]
    matches = [ re.search(pattern, name) for name in names ]
    results = [ f"{match.group(1)}-{match.group(2)}" for match in matches ]
    old_fns = [ f"{IN_DIR}{fn}" for fn in names ]
    new_fns = [ f"{IN_DIR}{name}.xlsx" for name in results ]

    for (old_fn, new_fn) in zip(old_fns, new_fns):
        subprocess.run(["cp", f"{old_fn}", f"{new_fn}"]) 