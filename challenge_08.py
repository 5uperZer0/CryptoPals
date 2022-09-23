# Taken from the Cryptopals Guided Tour Series by NCC Group Global
from challenge_06 import calculate_hamming_distance

BLOCK_SIZE = 16


def bytes_to_chunks(bytes_in: bytes, chunk_size: int) -> list[bytes]:
    return [bytes_in[i: i+chunk_size] for i in range(0, len(bytes_in), chunk_size)]


def detect_ecb(ct: bytes, block_size: int = BLOCK_SIZE) -> bool:
    num_of_blocks = len(ct) // block_size
    num_unique_blocks = len(set(bytes_to_chunks(ct, block_size)))
    if num_of_blocks != num_unique_blocks:
        return True
    return False


if __name__ == "__main__":
    with open("challenge_08_text.txt") as f:
        ct_list = [bytes.fromhex(line.strip()) for line in f]

    for i, line in enumerate(ct_list):
        if detect_ecb(line):
            print(f"Line {line} contains repeated blocks and may use ecb")
