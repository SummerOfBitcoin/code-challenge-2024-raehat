import ecdsa
from hashlib import sha256
import hashlib
from ecdsa.util import sigdecode_der
import sys

def ecdsa_verify(_sig, _message, _pubKey):
    sig = bytes.fromhex(_sig)
    message = bytes.fromhex(_message)
    pubKey = _pubKey
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(pubKey), curve=ecdsa.SECP256k1, hashfunc=sha256)
    ans = False
    try:
        ans = vk.verify(sig, message, hashlib.sha256, sigdecode=sigdecode_der)
    except Exception as e:
        print(e)
    return ans