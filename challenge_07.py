from Crypto.Cipher import AES
from base64 import b64decode
from challenge_09 import pkcs7_padding, pkcs7_strip


def decrypt_AES_128_ECB(key: bytes, ct: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return pkcs7_strip(cipher.decrypt(ct))      # Return message and strip any padding


def encrypt_AES_128_ECB(key: bytes, pt: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_padding(pt, len(key)))      # Add padding then encrypt


if __name__ == "__main__":
    with open("challenge_07_text.txt", "rb") as f:
        b64_ct = f.read()
    ct = b64decode(b64_ct)
    key = b'YELLOW SUBMARINE'
    pt = decrypt_AES_128_ECB(key, ct)
    new_ct = encrypt_AES_128_ECB(key, pt)
    new_pt = decrypt_AES_128_ECB(key, new_ct)
    print(new_pt)
