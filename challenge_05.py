def repeating_key_xor(pt: str, key: str) -> bytes:
    key_len = len(key)
    ct = []
    i = 0
    for character in pt:
        new_byte = hex(ord(character) ^ ord(key[i % key_len]))[2:]
        if len(new_byte) == 1:
            new_byte = "0" + new_byte
        ct.append(new_byte)
        i += 1
    return bytes.fromhex("".join(i for i in ct))


if __name__ == "__main__":
    plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    print(repeating_key_xor(plaintext, "ICE").hex())

