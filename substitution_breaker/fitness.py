import math
import re


class fintess_func:
    def __init__(self, alphabet: []):
        self.alphabet = alphabet

    def calculate_n_grams(self, text: bytes, pivot: int) -> []:
        n_grams = []
        for i in range(len(text) - pivot):
            n_grams.append(text[i:i + pivot])

        return n_grams

    def calc_fq(self, text: bytes, n_gram: bytes) -> int:
        fq = 0
        for i in range(len(text) - len(n_gram)):
            if text[i: i + len(n_gram)] == n_gram:
                fq += 1
        return fq

    def decrypt_with_key(self, text: bytes, key: bytes) -> bytes:
        decrypted = b''
        for byte in text:
            id = self.alphabet.index(byte)
            decrypted += bytes(key[id], 'ascii')
        return decrypted

    def aplay(self, text: bytes, trained: bytes, chromosome: bytes, pivot: int):
        source_grams = self.calculate_n_grams(trained, pivot)
        decrypted = self.decrypt_with_key(text, chromosome)
        processed_grams = self.calculate_n_grams(decrypted, pivot)
        fq_source = list([self.calc_fq(text, n_gram) if n_gram in source_grams else 0 for n_gram in processed_grams])
        fq_decrypted = list([self.calc_fq(decrypted, n_gram) for n_gram in processed_grams])
        smooth_if = lambda v: math.log2(v) if v != 0 else 0
        fitness = sum([smooth_if(fq[0]) * fq[1] for fq in zip(fq_source, fq_decrypted)])
        return fitness
