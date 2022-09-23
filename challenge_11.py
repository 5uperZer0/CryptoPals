# Used some code from "Cryptopals Set 2" from Hilbert on Youtube
from random import randint
from os import urandom
from challenge_10 import encrypt_aes_cbc
from challenge_07 import encrypt_AES_128_ECB
from challenge_08 import detect_ecb


class EncryptionOracleInterface:
    def encrypt(self, data: bytes) -> bytes:
        pass


class EncryptionOracle(EncryptionOracleInterface):
    def __init__(self, key_size: int):
        self.key = urandom(key_size)
        self.key_size = key_size
        self.history = []

    def encrypt(self, data: bytes) -> bytes:
        pt = urandom(randint(5, 10)) + data + urandom(randint(5, 10))
        if randint(0, 1):
            self.history.append('ECB')
            return encrypt_AES_128_ECB(self.key, pt)
        else:
            self.history.append('CBC')
            return encrypt_aes_cbc(self.key, pt, urandom(self.key_size))


def detect_ecb_cbc(oracle: type[EncryptionOracleInterface], data, key_len) -> str:
    ct = oracle.encrypt(data)
    num_of_blocks = len(ct) // key_len
    return 'ECB' if detect_ecb(ct, key_len) else 'CBC'


def main():
    key_len = 16
    oracle = EncryptionOracle(key_len)
    data = b'A' * 48
    detections = []

    for _ in range(100):
        detections.append(detect_ecb_cbc(oracle, data, key_len))

    print(f"Percentage correct: {100 * sum(1 if detections[i] == oracle.history[i] else 0 for i in range(100)) // 100}%")


if __name__ == "__main__":
    main()
