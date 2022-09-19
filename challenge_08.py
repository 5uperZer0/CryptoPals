# Taken from the Cryptopals Guided Tour Series by NCC Group Global


BLOCK_SIZE = 16


def bytes_to_chunks(bytes_in: bytes, chunk_size: int) -> list[bytes]:
    return [bytes_in[i: i+chunk_size] for i in range(0, len(bytes_in), chunk_size)]


if __name__ == "__main__":
    with open("challenge_08_text.txt") as f:
        ct_list = [bytes.fromhex(line.strip()) for line in f]

    for i, ct in enumerate(ct_list):
        num_of_blocks = len(ct) // BLOCK_SIZE
        num_unique_blocks = len(set(bytes_to_chunks(ct, BLOCK_SIZE)))
        repeated_blocks = num_of_blocks - num_unique_blocks
        if repeated_blocks == 0:
            continue
        else:
            print(f"Line {i} contains {repeated_blocks} repeated blocks and may use ecb")

