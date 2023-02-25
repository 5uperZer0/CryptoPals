from base64 import b64decode
from dataclasses import astuple
from math import floor
from challenge_03 import crack_xor_cipher


def calculate_hamming_distance(s1: bytes, s2: bytes) -> int:
    distance = 0
    assert len(s1) == len(s2)
    string_length = len(s1)
    for i in range(string_length):  # Loop through all bytes
        b1 = bin(s1[i])[2:]
        b2 = bin(s2[i])[2:]  # Removes the "0b" from the start of the byte
        if len(b2) > len(b1):
            b1 = "0" * (len(b2) - len(b1)) + b1  # Add padding if b2 is longer than b1
        else:
            b2 = "0" * (len(b1) - len(b2)) + b2  # Add padding if b1 is longer than b2
        distance += sum(i != j for i, j in zip(b1, b2))  # Calculate hamming distance between bytes
    return distance


def calculate_key_size(ct: bytes, ll: int, ul: int) -> int:
    best_distance = float('inf')
    best_size = ll
    for i in range(ll, ul + 1):
        num_of_groups = floor(len(ct) / i)  # Number of logical groupings of bytes

        current_dist = sum(calculate_hamming_distance(ct[group:group + i], ct[group + i:group + i * 2]) for
                           group in range(0, num_of_groups // 2, i * 2))  # Calculate Hamming distance for pairs

        # current_dist = (current_dist / num_of_groups) / i       # This was supposed to normalize, but I don't know how

        if current_dist < best_distance:
            best_distance = current_dist
            best_size = i

    return best_size


def find_repeating_xor_key(ct: bytes, ll: int, ul: int) -> bytes:
    block_size = calculate_key_size(ct, ll=ll, ul=ul)
    blocks = [[] for i in range(block_size)]  # Generate a list of lists as long as the key
    for i in range(len(ct)):
        blocks[i % block_size].append(ct[i])  # Sort ct characters into corresponding blocks
    key = bytes(astuple(crack_xor_cipher(bytes(block)))[1] for block in blocks)
    # The above line cracks each block as if it were its own message encrypted with a one byte key
    return key


def decode_with_key(ct: bytes, key: bytes) -> bytes:
    pt = []
    for i, byte in enumerate(ct):
        new_byte = hex(byte ^ key[i % len(key)])[2:]        # Byte = byte XOR'd with corresponding key byte
        if len(new_byte) == 1:
            new_byte = "0" + new_byte                       # Pad out byte
        pt.append(new_byte)
    return bytes.fromhex("".join(pt))                       # Join bytes and return


if __name__ == "__main__":
    with open("challenge_06_text.txt") as f:
        b64_ct = f.read()
        b64_ct = "".join(b64_ct.splitlines())
    ct = bytes(b64decode(b64_ct))
    key = find_repeating_xor_key(ct, 2, 40)
    print(decode_with_key(ct, key))
