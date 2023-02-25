def pkcs7_padding(b: bytes, block_size: int) -> bytes:
    padding_length = block_size - (len(b) % block_size)     # Padding length = block_size - remainder
    return b + bytes([padding_length]) * padding_length if padding_length != 0 else b + bytes([block_size]) * block_size
    # The above line adds {padding length} bytes of 0x{padding length} unless length = 0, in which case it returns x10


def pkcs7_strip(b: bytes) -> bytes:
    if all(i == b[-1] for i in b[-b[-1]:]):     # If the last {b[-1]} bytes equal {b[-1]}, remove them
        return b[: -b[-1]]
    else:
        return b        # Otherwise, b is not padded so just return it


if __name__ == "__main__":
    key = b'YELLOW SUBMARINE'
    print(pkcs7_padding(key, 20))
    print(pkcs7_strip(pkcs7_padding(key, 20)))
