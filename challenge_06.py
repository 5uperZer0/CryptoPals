from base64 import b64decode
from math import floor
from challenge_03 import crack_xor_cipher
from dataclasses import astuple


def calculate_hamming_distance(s1: bytes, s2: bytes) -> int:
    distance = 0
    string_length = len(s1)
    for i in range(string_length):
        b1 = bin(s1[i])[2:]
        b2 = bin(s2[i])[2:]
        if len(b2) > len(b1):
            b1 = "0" * (len(b2) - len(b1)) + b1
        else:
            b2 = "0" * (len(b1) - len(b2)) + b2
        distance += sum(i != j for i, j in zip(b1, b2))
    return distance


def calculate_key_size(ct: str, ll: int, ul: int) -> int:
    best_distance = float('inf')
    best_size = ll
    for i in range(ll, ul + 1):
        num_of_groups = floor(len(ct) / i)
        num_of_iters = floor(num_of_groups/2)
        current_dist = (sum(calculate_hamming_distance(ct[group:group + i], ct[group + i:group + i * 2]) for
                            group in range(0, num_of_iters * i, i*2)) / num_of_groups) / i

        if current_dist < best_distance:
            best_distance = current_dist
            best_size = i
    return best_size


def find_repeating_xor_key(ct: bytes, ll: int, ul: int) -> str:
    block_size = calculate_key_size(ct, ll=ll, ul=ul)
    blocks = [[] for i in range(block_size)]
    for i in range(len(ct)):
        blocks[i % block_size].append(ct[i])
    key = bytes(astuple(crack_xor_cipher(block))[1] for block in blocks)
    return key


def decode_with_key(ct: bytes, key: bytes) -> bytes:
    key_len = len(key)
    pt = []
    for i, byte in enumerate(ct):
        new_byte = hex(byte ^ key[i % key_len])[2:]
        if len(new_byte) == 1:
            new_byte = "0" + new_byte
        pt.append(new_byte)
    return bytes.fromhex("".join(pt))


if __name__ == "__main__":
    with open("challenge_06_text.txt") as f:
        b64_ct = f.read()
        b64_ct = "".join(b64_ct.splitlines())
    ct = b64decode(b64_ct)
    key = find_repeating_xor_key(ct, 2, 40)
    print(decode_with_key(ct, key))
