def repeating_key_xor(pt: str, key: str) -> bytes:
    key_len = len(key)
    ct = []
    for i, character in enumerate(pt):
        new_byte = hex(ord(character) ^ ord(key[i % key_len]))[2:]  # New byte = character ^ corresponding key character
        if len(new_byte) == 1:
            new_byte = "0" + new_byte       # Pad byte if necessary
        ct.append(new_byte)
    return bytes.fromhex("".join(ct))       # Return hex as bytes list


if __name__ == "__main__":
    plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    print(repeating_key_xor(plaintext, "ICE").hex())

