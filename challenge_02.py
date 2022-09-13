# Taken from the Cryptopals Guided Tour Series by NCC Group Global

def _xor_bytes(hex_1: bytes, hex_2: bytes, quiet=True, check_lens=False) -> bytes:
	if not quiet:
		print(hex_1, "@", hex_2)
	if check_lens and len(hex_1) != len(hex_2):
		raise ValueError("bytestring lengths aren't equal")
	return bytes(byte_1 ^ byte_2 for byte_1, byte_2 in zip(hex_1, hex_2))


def xor_bytes(*args: bytes, quiet=True, check_lens=False):
	assert len(args) > 0
	result = args[0]
	for arg in args[1:]:
		result = _xor_bytes(result, arg, quiet=quiet, check_lens=check_lens)
	return result


if __name__ == "__main__":
	print(xor_bytes(bytes.fromhex("1c0111001f010100061a024b53535009181c"),
					bytes.fromhex("686974207468652062756c6c277320657965"),
					quiet=False))

