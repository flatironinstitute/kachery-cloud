from ._client_keys import _get_client_keys_hex

def get_client_id():
    public_key_hex, _ = _get_client_keys_hex()
    return public_key_hex