def pkcs7_padding(b: bytes, block_size: int) -> bytes:
    padding_length = block_size - (len(b) % block_size)
    return b + bytes([padding_length]) * padding_length if padding_length != 0 else b + bytes([block_size]) * block_size


def pkcs7_strip(b: bytes) -> bytes:
    if all(i == b[-1] for i in b[-b[-1]:]):
        return b[: -b[-1]]
    else:
        return b


if __name__ == "__main__":
    key = b'YELLOW SUBMARINE'
    print(pkcs7_padding(key, 20))
    print(pkcs7_strip(pkcs7_padding(key, 20)))
