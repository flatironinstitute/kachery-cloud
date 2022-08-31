import os
import base64
import numpy as np
from .get_kachery_cloud_dir import get_kachery_cloud_dir

# {dir: {client_private_key_hex: '...', client_public_key_hex: '...}}
_global_client_keys_by_kachery_dir = {}

def _ephemeral_mode():
    return os.environ.get('KACHERY_CLOUD_EPHEMERAL') == 'TRUE'

def _get_client_keys_hex(): # public, private
    KACHERY_CLOUD_CLIENT_ID = os.getenv('KACHERY_CLOUD_CLIENT_ID', None)
    KACHERY_CLOUD_PRIVATE_KEY = os.getenv('KACHERY_CLOUD_PRIVATE_KEY', None)
    if KACHERY_CLOUD_CLIENT_ID is not None:
        if KACHERY_CLOUD_PRIVATE_KEY is None:
            raise Exception('Environment variable not set: KACHERY_CLOUD_PRIVATE_KEY (even though KACHERY_CLOUD_CLIENT_ID is set)')
    if KACHERY_CLOUD_CLIENT_ID is not None:
        return KACHERY_CLOUD_CLIENT_ID, KACHERY_CLOUD_PRIVATE_KEY
    # don't use sandbox directory for getting the keys, use the normal one
    kachery_cloud_dir = get_kachery_cloud_dir(respect_sandbox=False)
    kk = _global_client_keys_by_kachery_dir.get(kachery_cloud_dir, None)
    if kk is not None:
        return kk['client_public_key_hex'], kk['client_private_key_hex']
    private_key_fname = f'{kachery_cloud_dir}/private.pem'
    public_key_fname = f'{kachery_cloud_dir}/public.pem'
    if not os.path.exists(private_key_fname):
        _generate_client_keys()
    with open(private_key_fname, 'r') as f:
        private_key = f.read()
    with open(public_key_fname, 'r') as f:
        public_key = f.read()
    private_key_hex = _private_key_to_hex(private_key)
    public_key_hex = _public_key_to_hex(public_key)
    _global_client_keys_by_kachery_dir[kachery_cloud_dir] = {
        'client_private_key_hex': private_key_hex,
        'client_public_key_hex': public_key_hex
    }
    return public_key_hex, private_key_hex

def _generate_client_keys():
    kachery_cloud_dir = get_kachery_cloud_dir()
    public_key_fname = f'{kachery_cloud_dir}/public.pem'
    private_key_fname = f'{kachery_cloud_dir}/private.pem'
    if os.path.exists(public_key_fname):
        raise Exception('public.pem already exists')
    if os.path.exists(private_key_fname):
        raise Exception('private.pem already exists')
    public_key_hex, private_key_hex = _generate_keypair()
    public_key = _public_key_from_hex(public_key_hex)
    private_key = _private_key_from_hex(private_key_hex)
    with open(public_key_fname, 'w') as f:
        f.write(public_key)
    with open(private_key_fname, 'w') as f:
        f.write(private_key)
    os.chmod(private_key_fname, 0o600) # only owner can read and write

def _sign_message_as_client(msg: dict):
    public_key_hex, private_key_hex = _get_client_keys_hex()
    return _sign_message(msg, public_key_hex, private_key_hex)

ed25519PubKeyPrefix = "302a300506032b6570032100"
ed25519PrivateKeyPrefix = "302e020100300506032b657004220420"

def _public_key_to_hex(key: str) -> str:
    x = key.split('\n')
    if x[0] != '-----BEGIN PUBLIC KEY-----':
        raise Exception('Problem in public key format (1).')
    if x[2] != '-----END PUBLIC KEY-----':
        raise Exception('Problem in public key format (2).')
    ret = base64.b64decode(x[1]).hex()
    if not ret.startswith(ed25519PubKeyPrefix):
        raise Exception('Problem in public key format (3).')
    return ret[len(ed25519PubKeyPrefix):]

def _private_key_to_hex(key: str) -> str:
    x = key.split('\n')
    if x[0] != '-----BEGIN PRIVATE KEY-----':
        raise Exception('Problem in private key format (1).')
    if x[2] != '-----END PRIVATE KEY-----':
        raise Exception('Problem in private key format (2).')
    ret = base64.b64decode(x[1]).hex()
    if not ret.startswith(ed25519PrivateKeyPrefix):
        raise Exception('Problem in private key format (3).')
    return ret[len(ed25519PrivateKeyPrefix):]

def _public_key_from_hex(key_hex: str):
    a = base64.b64encode(bytes.fromhex(ed25519PubKeyPrefix + key_hex)).decode()
    return f'-----BEGIN PUBLIC KEY-----\n{a}\n-----END PUBLIC KEY-----'

def _private_key_from_hex(key_hex: str):
    a = base64.b64encode(bytes.fromhex(ed25519PrivateKeyPrefix + key_hex)).decode()
    return f'-----BEGIN PRIVATE KEY-----\n{a}\n-----END PRIVATE KEY-----'

def _deterministic_json_dumps(x: dict):
    import simplejson
    return simplejson.dumps(x, separators=(',', ':'), indent=None, allow_nan=False, sort_keys=True)

def _sha1_of_string(txt: str) -> str:
    import hashlib
    hh = hashlib.sha1(txt.encode('utf-8'))
    ret = hh.hexdigest()
    return ret

def _sign_message(msg: dict, public_key_hex: str, private_key_hex: str) -> str:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    msg_json = _deterministic_json_dumps(msg)
    msg_hash = _sha1_of_string(msg_json)
    msg_bytes = bytes.fromhex(msg_hash)
    privk = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_key_hex))
    pubk = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key_hex))
    signature = privk.sign(msg_bytes).hex()
    pubk.verify(bytes.fromhex(signature), msg_bytes)
    return signature

def _verify_signature(msg: dict, public_key_hex: str, signature: str):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    msg_json = _deterministic_json_dumps(msg)
    msg_hash = _sha1_of_string(msg_json)
    msg_bytes = bytes.fromhex(msg_hash)
    pubk = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key_hex))
    try:
        pubk.verify(bytes.fromhex(signature), msg_bytes)
    except:
        return False
    return True

def _generate_keypair():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    privk = Ed25519PrivateKey.generate()
    pubk = privk.public_key()
    private_key_hex = privk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    ).hex()
    public_key_hex = pubk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    ).hex()
    test_msg = {'a': 1}
    test_signature = _sign_message(test_msg, public_key_hex, private_key_hex)
    assert _verify_signature(test_msg, public_key_hex, test_signature)
    return public_key_hex, private_key_hex