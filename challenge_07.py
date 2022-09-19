from Crypto.Cipher import AES
from base64 import b64decode


def decode_AES_128_ECB(key: bytes, ct: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ct)


if __name__ == "__main__":
    with open("challenge_07_text.txt", "rb") as f:
        b64_ct = f.read()
    ct = b64decode(b64_ct)
    key = b'YELLOW SUBMARINE'
    print(decode_AES_128_ECB(key, ct))
