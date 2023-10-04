import os


def admin_delete_file(uri: str):
    """Delete a file from cloud bucket - admin only - only do this during batch cleanup"""
    if not uri.startswith('sha1://'):
        raise Exception('URI must start with sha1://')
    
    sha1 = uri.split('?')[0].split('/')[2]

    kachery_zone = os.environ.get('KACHERY_ZONE', 'default')
    payload = {
        'type': 'deleteFile',
        'hashAlg': 'sha1',
        'hash': sha1,
        'zone': kachery_zone
    }
    from ._kachery_gateway_request import _kachery_gateway_request
    response= _kachery_gateway_request(payload)
    if not response['success']:
        raise Exception(response['error'])