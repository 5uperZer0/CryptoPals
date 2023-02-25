# Some code taken from the Cryptopals Guided Tour Series by NCC Group Global

def _xor_bytes(hex_1: bytes, hex_2: bytes) -> bytes:
	return bytes(byte_1 ^ byte_2 for byte_1, byte_2 in zip(hex_1, hex_2))


def xor_bytes(*args: bytes):
	assert len(args) > 0						# Input validation
	result = args[0]
	for arg in args[1:]:
		result = _xor_bytes(result, arg)		# XOR all args with arg[0]
	return result


if __name__ == "__main__":
	print(xor_bytes(bytes.fromhex("1c0111001f010100061a024b53535009181c"),
					bytes.fromhex("686974207468652062756c6c277320657965")))
