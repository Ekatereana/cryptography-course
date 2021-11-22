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
