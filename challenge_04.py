from challenge_03 import crack_xor_cipher, ScoredGuess
from dataclasses import astuple


def find_and_crack_xor_cipher(cipher_file: bytes) -> ScoredGuess:
    with open(cipher_file) as f:
        strings = f.read()

        lines = strings.split("\n")
        best_guess = ScoredGuess()
        for line in lines:
            current_ciphertext = bytes.fromhex(line)
            guess = crack_xor_cipher(current_ciphertext)
            best_guess = min(best_guess, guess)
        return best_guess


if __name__ == "__main__":
    best_guess = find_and_crack_xor_cipher("challenge_04_text.txt")
    score, key, ciphertext, plaintext = astuple(best_guess)
    print(key)
    print(plaintext)


