import os
from typing import Union
import requests
import random
from .get_kachery_cloud_dir import get_kachery_cloud_dir


def load_file(uri: str) -> Union[str, None]:
    assert uri.startswith('ipfs://'), f'Invalid or unsupported URI: {uri}'
    a = uri.split('/')
    assert len(a) >= 3, f'Invalid or unsupported URI: {uri}'
    cid = a[2]

    kachery_cloud_dir = get_kachery_cloud_dir()
    parent_dir = f'{kachery_cloud_dir}/ipfs/{cid[0]}{cid[1]}/{cid[2]}{cid[3]}/{cid[4]}{cid[5]}'
    filename = f'{parent_dir}/{cid}'
    if os.path.exists(filename):
        return filename

    tmp_filename = filename + '.downloading'
    if os.path.exists(tmp_filename):
        raise Exception(f'Temporary file exists.')

    # url = f'https://{cid}.ipfs.dweb.link'
    # url = f'https://cloudflare-ipfs.com/ipfs/{cid}'
    url = f'https://kachery-cloud.mypinata.cloud/ipfs/{cid}'
    
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    tmp_filename = f'{filename}.tmp.{_random_string(8)}'
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(tmp_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    try:
        os.rename(tmp_filename, filename)
    except:
        if not os.path.exists(filename): # maybe some other process beat us to it
            raise Exception(f'Unexpected problem moving file {tmp_filename}')
    return filename

def _random_string(num_chars: int) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(num_chars))