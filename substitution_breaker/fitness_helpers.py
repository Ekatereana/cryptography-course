import math
import re

alphabet_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

alphabet_order_ord = list([ord(letter) for letter in alphabet_order])


def fitness_func(text: bytes, chromosome: bytes, pivot: int):
    pattern = r'[0-9/\:\[\]\.\"\?\;\-]'
    with open("../assets/train_text.txt", 'r', encoding="utf-8") as t_f:
        source = bytes(re.sub(pattern, '', t_f.read().upper()), "utf-8")

    source_grams = calculate_n_grams(source, pivot)
    decrypted = decrypt_with_key(text, chromosome)
    processed_grams = calculate_n_grams(decrypted, pivot)
    fq_source = list([calc_fq(text, n_gram) if n_gram in source_grams else 0 for n_gram in processed_grams])
    fq_decrypted = list([calc_fq(decrypted, n_gram) for n_gram in processed_grams])
    smooth_if = lambda v: math.log2(v) if v != 0 else 0
    fitness = sum([smooth_if(fq[0]) * fq[1] for fq in zip(fq_source, fq_decrypted)])
    return fitness


def calculate_n_grams(text: bytes, pivot: int) -> []:
    n_grams = []
    for i in range(len(text) - pivot):
        n_grams.append(text[i:i + pivot])

    return n_grams


def calc_fq(text: bytes, n_gram: bytes) -> int:
    fq = 0
    for i in range(len(text) - len(n_gram)):
        if text[i: i + len(n_gram)] == n_gram:
            fq += 1
    return fq


def decrypt_with_key(text: bytes, key: bytes) -> bytes:
    decrypted = b''
    print(len(key))
    for byte in text:
        id = alphabet_order_ord.index(byte)
        decrypted += bytes(key[id], 'ascii')
    return decrypted
