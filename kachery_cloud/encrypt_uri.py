from ._access_group_encrypt import _access_group_encrypt, _access_group_decrypt


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
    elif uri.startswith('sha1-enc://'):
        aa = uri.split('?')[0].split('/')[2]
        bb = aa.split('.')
        assert len(bb) == 2
        access_group_str = bb[1]
        assert access_group_str.startswith('ag_')
        access_group0 = access_group_str[3:]
        if access_group0 == access_group:
            return uri
        uri2 = decrypt_uri(uri)
        return encrypt_uri(uri2, access_group=access_group)
    else:
        raise Exception(f'Not able to encrypt URI: {uri}')

def decrypt_uri(uri: str):
    aa = uri.split('?')[0].split('/')[2]
    bb = aa.split('.')
    assert len(bb) == 2
    sha1_enc = bb[0]
    access_group_str = bb[1]
    assert access_group_str.startswith('ag_')
    access_group = access_group_str[3:]
    sha1 = _access_group_decrypt(sha1_enc, access_group=access_group)
    qstr = f'?{uri.split("?")[1]}' if len(uri.split('?')) > 1 else ''
    return f'sha1://{sha1}{qstr}'