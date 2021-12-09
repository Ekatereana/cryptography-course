def calculate_n_grams(text: bytes, pivot: int, with_pos: bool = False):
    n_grams = []
    positions = []
    for i in range(len(text) - pivot):
        n_grams.append(text[i:i + pivot])
        positions.append(i)

    if with_pos:
        return zip(n_grams, positions)
    return n_grams


def calc_fq(text: bytes, n_gram: bytes) -> int:
    fq = 0
    for i in range(len(text) - len(n_gram)):
        if text[i: i + len(n_gram)] == n_gram:
            fq += 1
    return fq


def get_nth_letter(text: [], start: int, nth: int) -> []:
    return bytes([text[i] for i in range(start, len(text), nth)])
