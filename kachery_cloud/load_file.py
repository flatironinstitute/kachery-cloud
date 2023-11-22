import json
import os
import shutil
from typing import Union
import requests
import random
import time

from .get_kachery_cloud_dir import get_kachery_cloud_dir
from .store_file_local import _compute_file_hash
from ._fs_operations import _makedirs
from ._load_github_file import _load_github_file, _load_http_file


def load_file(uri: str, *, verbose: bool=False, local_only: bool=False, dest: Union[None, str]=None, _get_info: bool=False, do_request: Union[bool, None]=None) -> Union[str, dict, None]:
    if uri.startswith('gh://'):
        return _load_github_file(uri)
    
    if uri.startswith('http://') or uri.startswith('https://'):
        return _load_http_file(uri)

    if local_only:
        return load_file_local(uri, dest=dest)
    if uri.startswith('/'):
        if _get_info:
            raise Exception('Cannot use _get_info for this uri')
        if os.path.exists(uri):
            if dest is not None:
                shutil.copyfile(uri, dest)
                return dest
            return uri
        else:
            return None
    if uri.startswith('sha1://'):
        if not _get_info:
            x = load_file_local(uri, dest=dest)
            if x is not None:
                return x
        sha1 = uri.split('?')[0].split('/')[2]
        fname = _load_sha1_file_from_cloud(sha1, verbose=verbose, dest=dest, _get_info=_get_info)
        if fname is not None:
            return fname
        resource_url = os.getenv('KACHERY_RESOURCE_URL', None)
        if resource_url is not None and do_request is not False:
            from .request_file import request_file
            while True:
                # the timeout refers to how long we will wait for the file to upload before returning
                rr = request_file(uri, resource_url=resource_url, timeout_sec=5, ignore_local=True, ignore_bucket=True)
                if rr.errored:
                    print(f'Error: {rr.error_message}')
                    return None
                if not rr.found:
                    return None
                if rr.completed:
                    print('Downloading file')
                    return load_file(uri, dest=dest, do_request=False) # set do_request=False to avoid possibility of infinnite recursion
                if rr.queued:
                    print('File queued for upload')
                elif rr.running:
                    print('File uploading')
                elif rr.error_message:
                    raise Exception('Error uploading file.')
                time.sleep(4)
        else:
            return None
    
    if uri.startswith('zenodo://') or uri.startswith('zenodo-sandbox://'):
        x = load_file_local(uri, dest=dest)
        if x is not None:
            return x
        return _load_zenodo_file_from_cloud(uri, dest=dest)

    if _get_info:
        raise Exception('Cannot use _get_info for this uri')

    assert f'Invalid or unsupported URI: {uri}'

def load_file_info(uri: str) -> dict:
    return load_file(uri, _get_info=True)

def _load_zenodo_file_from_cloud(uri: str, *, dest: Union[None, str]=None):
    sandbox = uri.startswith('zenodo-sandbox://')
    aa = uri.split('?')[0].split('/')
    z_record_id = aa[2]
    z_file_name = '/'.join(aa[3:])

    record_url = f'https://{"sandbox.zenodo" if sandbox else "zenodo"}.org/api/records/{z_record_id}'
    req_resp = requests.get(record_url)
    if req_resp.status_code != 200:
        raise Exception(f'Error downloading zenodo record info ({req_resp.status_code}) {req_resp.reason}: {req_resp.text}')
    resp = req_resp.json()
    if 'files' not in resp:
        raise Exception('Error getting zenodo record')
    cc = [f for f in resp['files'] if f.get('filename', f.get('key', '')) == z_file_name]
    if len(cc) == 0:
        raise Exception('File not found in zenodo record')
    dd = cc[0]
    url = dd['links'].get('download', dd['links'].get('self'))
    
    kachery_cloud_dir = get_kachery_cloud_dir()
    filename = f'{kachery_cloud_dir}/{"zenodo-sandbox" if sandbox else "zenodo"}/{z_record_id}/{z_file_name}'
    parent_dir = os.path.dirname(filename)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    tmp_filename = f'{filename}.tmp.{_random_string(8)}'
    with requests.get(url, stream=True) as r:
        if r.status_code == 404:
            raise Exception(f'Unexpected: file not found: {url}')
        r.raise_for_status()
        with open(tmp_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    try:
        os.rename(tmp_filename, filename)
        # _chmod_file(filename)
    except:
        if not os.path.exists(filename): # maybe some other process beat us to it
            raise Exception(f'Unexpected problem moving file {tmp_filename}')
    if dest is not None:
        shutil.copyfile(filename, dest)
        return dest
    return filename

def _load_sha1_file_from_cloud(sha1: str, *, verbose: bool, dest: Union[None, str]=None, _get_info: bool=False) -> Union[str, dict, None]:
    kachery_zone = os.environ.get('KACHERY_ZONE', 'default')
    payload = {
        'type': 'findFile',
        'hashAlg': 'sha1',
        'hash': sha1,
        'zone': kachery_zone
    }
    from ._kachery_gateway_request import _kachery_gateway_request
    response= _kachery_gateway_request(payload)
        
    found = response['found']
    uri = f'sha1://{sha1}'
    if found:
        url = response['url']
    else:
        return None

    if _get_info:
        # we don't want the user to get the idea they should use the URL directly!
        del response['url']
        return response

    kachery_cloud_dir = get_kachery_cloud_dir()
    e = sha1
    parent_dir = f'{kachery_cloud_dir}/sha1/{e[0]}{e[1]}/{e[2]}{e[3]}/{e[4]}{e[5]}'
    filename = f'{parent_dir}/{sha1}'
    if verbose:
        print(f'Loading file from kachery cloud: {uri}') 
    if not os.path.exists(parent_dir):
        _makedirs(parent_dir)
    tmp_filename = f'{filename}.tmp.{_random_string(8)}'
    with requests.get(url, stream=True) as r:
        if r.status_code == 404:
            raise Exception(f'Unexpected: file not found in bucket: {url}')
        r.raise_for_status()
        with open(tmp_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    try:
        os.rename(tmp_filename, filename)
        # _chmod_file(filename)
    except:
        if not os.path.exists(filename): # maybe some other process beat us to it
            raise Exception(f'Unexpected problem moving file {tmp_filename}')
    if dest is not None:
        shutil.copyfile(filename, dest)
        return dest
    return filename

def load_file_local(uri: str, *, dest: Union[None, str]=None) -> Union[str, None]:
    if uri.startswith('zenodo://') or uri.startswith('zenodo-sandbox://'):
        sandbox = uri.startswith('zenodo-sandbox://')
        aa = uri.split('?')[0].split('/')
        z_record_id = aa[2]
        z_file_name = '/'.join(aa[3:])

        kcdir = get_kachery_cloud_dir()
        pp = f'{kcdir}/{"zenodo-sandbox" if sandbox else "zenodo"}/{z_record_id}/{z_file_name}'
        if os.path.exists(pp):
            if dest is not None:
                shutil.copyfile(pp, dest)
                return dest
            return pp
        else:
            return None

    query = _get_query_from_uri(uri)
    assert uri.startswith('sha1://'), f'Invalid local URI: {uri}'
    a = uri.split('?')[0].split('/')
    assert len(a) >= 3, f'Invalid or unsupported URI: {uri}'
    sha1 = a[2]

    kachery_cloud_dir = get_kachery_cloud_dir()

    s = sha1
    parent_dir = f'{kachery_cloud_dir}/sha1/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}'
    filename = f'{parent_dir}/{sha1}'
    if os.path.exists(filename):
        if dest is not None:
            shutil.copyfile(filename, dest)
            return dest
        return filename
    
    if 'location' in query:
        location = query['location']
        if os.path.isabs(location) and os.path.exists(location):
            sha1_2 = _compute_file_hash(location, 'sha1')
            if sha1_2 == sha1:
                if dest is not None:
                    shutil.copyfile(location, dest)
                    return dest
                return location
    
    # check for linked file
    s = sha1
    linked_file_record_parent_dir = f'{kachery_cloud_dir}/linked_files/sha1/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}'
    linked_file_record_path = f'{linked_file_record_parent_dir}/{sha1}'
    if os.path.exists(linked_file_record_path):
        with open(linked_file_record_path, 'r') as f:
            a_txt = f.read()
        a = json.loads(a_txt)
        path0 = a['path']
        size0 = a['size']
        mtime0 = a['mtime']
        if os.path.exists(path0):
            if os.path.getsize(path0) == size0 and os.stat(path0).st_mtime == mtime0:
                if dest is not None:
                    shutil.copyfile(path0, dest)
                    return dest
                return path0
            if (os.path.getsize(path0) == size0) and (_compute_file_hash(path0, algorithm='sha1') == sha1):
                # file mtime has been updated, but hash is still the same
                with open(linked_file_record_path, 'w') as f:
                    f.write(json.dumps({
                        'path': path0,
                        'size': os.path.getsize(path0),
                        'mtime': os.stat(path0).st_mtime,
                        'sha1': sha1
                    }))
                if dest is not None:
                    shutil.copyfile(path0, dest)
                    return dest
                return path0
            else:
                print(f'Warning: sha1 of linked file has changed: {path0} {uri}')
    
    return None

def _get_jot_value(jot_id):
    jot_url = 'https://jot.figurl.org/api/jot'
    req = {
        'type': 'getJotValue',
        'jotId': jot_id
    }
    resp = requests.post(jot_url, json=req)
    if resp.status_code != 200:
        raise Exception(f'Error getting jot value: ({resp.status_code}) {resp.reason}: {resp.text}')
    response = resp.json()
    if response['type'] != 'getJotValue':
        raise Exception('Unexpected problem getting jot value')
    return response['value']

def _get_query_from_uri(uri: str):
    a = uri.split('?')
    ret = {}
    if len(a) < 2: return ret
    b = a[1].split('&')
    for c in b:
        d = c.split('=')
        if len(d) == 2:
            ret[d[0]] = d[1]
    return ret

def _random_string(num_chars: int) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(num_chars))