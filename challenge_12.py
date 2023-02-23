from base64 import b64decode
from os import urandom

from challenge_07 import encrypt_AES_128_ECB
from challenge_11 import EncryptionOracleInterface

GLOBAL_KEY = urandom(16)


class EncryptionOracle(EncryptionOracleInterface):
    def __init__(self):
        self.key = GLOBAL_KEY
        self.secret = b64decode(
            b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK ")

    def encrypt(self, data: bytes) -> bytes:
        pt = data + self.secret
        return encrypt_AES_128_ECB(self.key, pt + self.secret)


def alternate_calculate_key_size(oracle: type[EncryptionOracleInterface]):
    i = 1
    while True:
        ct = list(oracle.encrypt(b"A" * (i + 1) * 2))
        if all(j == k for j, k in zip(ct[0:i], ct[i + 1: (i * 2) + 1])):
            ct = list(oracle.encrypt(b"A" * (i + 1) * 4))
            if all(j == k for j, k in zip(ct[0:i], ct[i + 1: (i * 2) + 1])):
                return i + 1
        else:
            i += 1


# This version is taken from Hilbert's Cryptopals Set 2 video on Youtube
def calculate_key_size(oracle: type[EncryptionOracleInterface]):
    test = b''
    base_len = len(oracle.encrypt(test))
    new_len = base_len

    while new_len == base_len:
        test += b'A'
        new_len = len(oracle.encrypt(test))

    return new_len - base_len


def break_ecb_alternate(oracle: type[EncryptionOracleInterface]):
    key_len = calculate_key_size(oracle)
    ct = oracle.encrypt(b'A' * key_len)
    dict_list = []
    # if detect_ecb(ct, key_len):
    for position in range(key_len):
        temp_dict = {}
        for i in range(256):
            new_ct = oracle.encrypt(b"A" * position + i.to_bytes(1, byteorder='big') + b"A" * (key_len - (position + 1)))
            temp_dict[new_ct[position]] = i
        dict_list.append(temp_dict.copy())

    pt = [hex(dict_list[i % key_len][byte])[2:] for i, byte in enumerate(ct)]
    pt = ["0" + new_byte for new_byte in pt if len(new_byte) == 1]
    return bytes.fromhex("".join(i for i in pt))


def break_ecb(oracle: type[EncryptionOracleInterface]):
    


if __name__ == "__main__":
    oracle = EncryptionOracle()
    print(break_ecb(oracle))
