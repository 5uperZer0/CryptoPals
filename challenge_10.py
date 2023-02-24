from challenge_07 import encrypt_AES_128_ECB, decrypt_AES_128_ECB
from challenge_02 import xor_bytes
from challenge_09 import pkcs7_padding, pkcs7_strip
from base64 import b64decode


def encrypt_aes_cbc(key: bytes, pt: bytes, iv: bytes) -> bytes:
    key_len = len(key)
    local_pt = pkcs7_padding(pt, key_len)

    pt_blocks = [local_pt[inc: + key_len] for inc in range(0, len(local_pt), key_len)]
    ct_blocks = []
    for i, block in enumerate(pt_blocks):
        if i == 0:
            prev_block = iv
        else:
            prev_block = ct_blocks[-1]
        ct_blocks.append(encrypt_AES_128_ECB(key, xor_bytes(block, prev_block)))
    return b''.join(ct_blocks)


def decrypt_aes_cbc(key: bytes, ct: bytes, iv: bytes) -> bytes:
    key_len = len(key)
    ct_blocks = [ct[inc: inc + key_len] for inc in range(0, len(ct), key_len)]
    pt_blocks = []
    for i, block in reversed(list(enumerate(ct_blocks))):
        if i == 0:
            prev_block = iv
        else:
            prev_block = ct_blocks[i - 1]
        pt_blocks.append(xor_bytes(decrypt_AES_128_ECB(key, block), prev_block))

    return pkcs7_strip(b''.join(reversed(pt_blocks)))


if __name__ == "__main__":
    with open("challenge_10_text.txt", "rb") as f:
        b64_ct = f.read()
    ct = b64decode(b64_ct)
    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * len(key)
    print(decrypt_aes_cbc(key, ct, iv))
