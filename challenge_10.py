from challenge_07 import encrypt_AES_128_ECB, decrypt_AES_128_ECB
from challenge_02 import xor_bytes
from challenge_09 import pkcs7_padding, pkcs7_strip
import challenge_08
from base64 import b64decode


def encrypt_aes_cbc(key: bytes, pt: bytes, iv: bytes) -> bytes:
    key_len = len(key)
    local_pt = pkcs7_padding(pt, key_len)
    pt_blocks = challenge_08.bytes_to_chunks(local_pt, key_len)
    ct_blocks = []
    prev_block = iv
    for block in pt_blocks:
        ct = encrypt_AES_128_ECB(key, xor_bytes(block, prev_block))
        ct_blocks.append(ct)
        prev_block = ct

    return b''.join(ct_blocks)


def decrypt_aes_cbc(key: bytes, ct: bytes, iv: bytes) -> bytes:
    ct_blocks = challenge_08.bytes_to_chunks(ct, len(key))

    pt_blocks = []
    prev_block = iv
    for block in ct_blocks:
        pt = xor_bytes(decrypt_AES_128_ECB(key, block), prev_block)
        pt_blocks.append(pt)
        prev_block = block

    return pkcs7_strip(b''.join(pt_blocks))


if __name__ == "__main__":

    with open("challenge_10_text.txt", "rb") as f:
        b64_ct = f.read()
    ct = b64decode(b64_ct)

    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * len(key)

    decrypted = decrypt_aes_cbc(key, ct, iv)
    print(decrypted)
    re_encrypted = encrypt_aes_cbc(key, decrypted, iv)
    print(decrypt_aes_cbc(key, re_encrypted, iv))

