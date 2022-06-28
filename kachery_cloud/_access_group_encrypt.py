from ._kacherycloud_request import _kacherycloud_request


def _access_group_encrypt(text: str, *, access_group: str):
    payload = {
        'type': 'accessGroupEncrypt',
        'accessGroupId': access_group,
        'text': text
    }
    response = _kacherycloud_request(payload)
    return response['encryptedText']

def _access_group_decrypt(encrypted_text: str, *, access_group: str):
    payload = {
        'type': 'accessGroupDecrypt',
        'accessGroupId': access_group,
        'encryptedText': encrypted_text
    }
    response = _kacherycloud_request(payload)
    return response['decryptedText']