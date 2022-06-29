from ._access_group_encrypt import _access_group_encrypt


def encrypt_uri(uri: str, *, access_group: str):
    if uri.startswith('sha1://'):
        a = uri.split('?')
        if len(a) < 2: a.append('')
        querystr = a[1]
        b = a[0].split('/')
        sha1 = b[2]
        sha1_enc = _access_group_encrypt(sha1, access_group=access_group)
        querystr_plus = f'?{querystr}' if len(querystr) > 0 else ''
        return f'sha1-enc://{sha1_enc}.ag_{access_group}{querystr_plus}'
    else:
        raise Exception(f'Not able to encrypt URI: {uri}')