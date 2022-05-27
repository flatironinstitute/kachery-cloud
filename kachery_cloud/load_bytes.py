import os
import sys
from typing import Union
from .load_file import load_file


# returns None if write_to_stdout is True
def load_bytes(uri: str, start: Union[int, None], end: Union[int, None], *, write_to_stdout=False) -> bytes: 
    local_path = load_file(uri)
    if local_path is None:
        return None
    
    return _load_bytes_from_local_file(local_path, start=start, end=end, write_to_stdout=write_to_stdout)

def _load_bytes_from_local_file(local_fname: str, *, start: Union[int, None]=None, end: Union[int, None]=None, write_to_stdout: bool=False) -> bytes:
    size0 = os.path.getsize(local_fname)
    if start is None:
        start = 0
    if end is None:
        end = size0
    if start < 0 or start > size0 or end < start or end > size0:
        raise Exception('Invalid start/end range for file of size {}: {} - {}'.format(size0, start, end))
    if start == end:
        return bytes()
    with open(local_fname, 'rb') as f:
        f.seek(start)
        if write_to_stdout:
            ii = start
            while ii < end:
                nn = min(end - ii, 4096)
                data0 = f.read(nn)
                ii = ii + nn
                sys.stdout.buffer.write(data0)
            return None
        else:
            return f.read(end-start)