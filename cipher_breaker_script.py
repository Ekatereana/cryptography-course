# dictionary in human mode
dict_eng_fq = {
    "e": 11.1607,
    "a": 8.4966,
    "r": 7.5809,
    "i": 7.5448,
    "o": 7.1635,
    "t": 6.9509,
    "n": 6.6544,
    "s": 5.7351,
    "l": 5.4893,
    "c": 4.5388,
    "u": 3.6308,
    "d": 3.3844,
    "p": 3.1671,
    "m": 3.0129,
    "h": 3.0034,
    "g": 2.4705,
    "b": 2.0720,
    "f": 1.8121,
    "y": 1.7779,
    "w": 1.2899,
    "k": 1.1016,
    "v": 1.0074,
    "x": 0.2902,
    "z": 0.2722,
    "j": 0.1965,
    "q": 0.1962
}

eng_letter_fq = list(dict_eng_fq.values())


def calc_letter_fq(text, l):
    return text.count(ord(l)) * 100 / len(text)


def calc_fitting_q(text):
    # calculate fq of letters in encripted text
    text_letter_fq = [calc_letter_fq(text, l) for l in dict_eng_fq.keys()]
    # f_lg -- frequency of letter in english
    # f_tx -- in the text
    return sum([abs(f_lg - f_tx) for f_lg, f_tx in zip(eng_letter_fq, text_letter_fq)]) / len(eng_letter_fq)

    if __name__ == '__main__':
        print('Hey we start')
