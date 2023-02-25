# Taken from the Cryptopals Guided Tour Series by NCC Group Global

from dataclasses import dataclass, astuple
from typing import Optional
from challenge_02 import xor_bytes

frequencies = {'a': 0.07566239439048221,
               'b': 0.013701936892924881,
               'c': 0.026047473992758204,
               'd': 0.048083223173745616,
               'e': 0.13156790620150582,
               'f': 0.024464049658026323,
               'g': 0.016618771193746766,
               'h': 0.05589114316914765,
               'i': 0.061509282142651875,
               'j': 0.0012385769297086039,
               'k': 0.004968676360710386,
               'l': 0.036214724984194493,
               'm': 0.02958503362262199,
               'n': 0.06962469107419966,
               'o': 0.07211333984711765,
               'p': 0.017113052474280133,
               'q': 0.0009282142651876545,
               'r': 0.05967584343927812,
               's': 0.05986263578366573,
               't': 0.08560262084027817,
               'u': 0.029731593769756884,
               'v': 0.010882809356859589,
               'w': 0.021185125581929996,
               'x': 0.0019426403816311282,
               'y': 0.02231450083338123,
               'z': 0.000614977872291511}


@dataclass(order=True)
class ScoredGuess:
    score: float = float("inf")
    key: Optional[bytes] = None
    ciphertext: Optional[bytes] = None
    plaintext: Optional[bytes] = None


def crack_xor_cipher(ct: bytes) -> ScoredGuess:
    best_guess = ScoredGuess()

    ct_len = len(ct)
    ct_freqs = {b: ct.count(b) / ct_len for b in range(256)}

    for candidate_key in range(256):  # Loop through all possible byte values
        score = 0
        for letter, frequency_expected in frequencies.items():
            score += abs(frequency_expected - ct_freqs[ord(letter) ^ candidate_key])  # Increase score per degree of
            # separation between expected and real outcomes
        guess = ScoredGuess(score, candidate_key)
        best_guess = min(best_guess, guess)     # Choose the guess with the lowest score

        best_guess.ciphertext = ct
        best_guess.plaintext = xor_bytes(ct, bytes([best_guess.key]) * len(ct))     # Fill out the rest of the fields

    return best_guess


if __name__ == "__main__":
    ciphertext = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    best_guess = crack_xor_cipher(ciphertext)
    score, key, ciphertext, plaintext = astuple(best_guess)

    print(key)
    print(plaintext)
