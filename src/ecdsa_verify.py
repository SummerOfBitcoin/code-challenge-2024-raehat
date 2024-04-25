import ecdsa
from hashlib import sha256
import hashlib
from ecdsa.util import sigdecode_der

def ecdsa_verify(_sig, _message, _pubKey):
    sig = bytes.fromhex(_sig)
    message = bytes.fromhex(_message)
    pubKey = _pubKey
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(pubKey), curve=ecdsa.SECP256k1, hashfunc=sha256)
    return vk.verify(sig, message, hashlib.sha256, sigdecode=sigdecode_der)