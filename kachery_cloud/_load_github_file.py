import requests
from .TemporaryDirectory import TemporaryDirectory


def _load_github_file(uri: str):
    from .store_file_local import store_file_local
    from .load_file import load_file_local
    
    user_name, repo_name, branch_name, file_name = _parse_github_uri(uri)
    url = f'https://raw.githubusercontent.com/{user_name}/{repo_name}/{branch_name}/{file_name}'
    with TemporaryDirectory(prefix='load_github_file') as tmpdir:
        tmp_filename = f'{tmpdir}/file.dat'
        with requests.get(url, stream=True) as r:
            if r.status_code == 404:
                raise Exception(f'File not found: {url}')
            r.raise_for_status()
            with open(tmp_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        uri = store_file_local(tmp_filename)
        return load_file_local(uri)

def _parse_github_uri(uri: str):
    if not uri.startswith('gh://'):
        raise Exception(f'Invalid github URI: {uri}')
    a = uri.split('/')
    if len(a) < 6:
        raise Exception(f'Invalid github URI: {uri}')
    user_name = a[2]
    repo_name = a[3]
    branch_name = a[4]
    file_name = '/'.join(a[5:])
    return user_name, repo_name, branch_name, file_name