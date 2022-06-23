import sys
import os
from .load_file import load_file

def cat_file(uri: str):
    old_stdout = sys.stdout
    sys.stdout = None

    local_fname = load_file(uri)

    sys.stdout = old_stdout

    if local_fname is None:
        return

    with open(local_fname, 'rb') as f:
        while True:
            data = os.read(f.fileno(), 4096)
            if len(data) == 0:
                break
            os.write(sys.stdout.fileno(), data)
