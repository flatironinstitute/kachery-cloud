from ._client_keys import _get_client_keys_hex

def get_client_id(generate_if_missing: bool=False) -> str:
    public_key_hex, _ = _get_client_keys_hex(generate_if_missing=generate_if_missing)
    return public_key_hex