from ._client_keys import _get_client_public_key_hex

def get_client_id():
    return _get_client_public_key_hex()