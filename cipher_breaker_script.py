import re
import codecs
import base64
import matplotlib.pyplot as plt

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
eng_letters = list([ord(l) for l in dict_eng_fq.keys()])


# solve single byte XOR cipher

def decode_single_byte_cipher(text: bytes):
    for k in range(255):
        try:
            print(single_byte_xor(text, k).decode("utf-8"))
        except UnicodeDecodeError:
            continue


def single_byte_xor(text: bytes, key: int):
    return bytes([el ^ key for el in text])


# solve second task
# def get_key_length(encoded):
#     shifts = []
#     c_ids = []
#     for shift in range(1, 12):
#         t_matrix = shift_text(encoded, shift)
#         shifts.append(shift)
#         c_ids.append(id_of_coincidence(t_matrix))
#     return shifts, c_ids
#
#
# def shift_text(text, t):
#     return list([text[i * t] for i in range(0, len(text) // t)])
#
#
# def id_of_coincidence(origin):
#     fqs = [get_fq_letter(l, origin) for l in eng_letters]
#     return sum([fq * (fq - 1) for fq in fqs]) / (len(origin) * (len(origin) - 1))


def get_fq_letter(letter, text):
    amount = 0
    for i in text:
        if letter == i:
            amount += 1
    return amount


def get_key_length(text):
    sizes = []
    h_distance = []

    for shift in range(1, 12):
        to_average = []
        start = 0
        end = start + shift
        while end + shift <= len(text):
            first_chunk = text[start:end]
            second_chunk = text[end:end + shift]
            distance = calc_hamming_dist(first_chunk, second_chunk)
            normalized = distance / shift
            to_average.append(normalized)
            start = end + shift
            end = start + shift
            to_average.append(normalized)

        average = sum(to_average) / len(to_average)
        sizes.append(shift)
        h_distance.append(average)

    return sizes, h_distance


def calc_hamming_dist(f_chunk: bytes, s_chunk: bytes) -> int:
    assert len(f_chunk) == len(s_chunk)

    distance = 0
    for enc in zip(f_chunk, s_chunk):
        xor = enc[0] ^ enc[1]
        step = 0
        while xor > 0:
            step += xor & 1
            xor >>= 1
        distance += step

    return distance


def get_key_word(text: bytes, key: int) -> str:
    dummy_criteria = 'ETAOIN SHRDLU'
    matrix = split_into_key_matrix(text, key)
    key_word = ''

    for chunk in matrix:
        highest_score = 0
        curr_key_letter = ''

        for symbol in range(255):
            xor_ed = [symbol ^ b for b in chunk]

            try:
                str_xor = bytes(xor_ed).decode("ascii")
                score = 0
                for char in str_xor.upper():
                    score += 1 if char in dummy_criteria else 0

                if score > highest_score:
                    highest_score = score
                    curr_key_letter = chr(symbol)
            except UnicodeDecodeError as err:
                continue
        key_word += curr_key_letter
    return key_word


def split_into_key_matrix(text: bytes, key_length: int) -> []:
    matrix = list([[] for i in range(key_length)])
    chunk_num = 0
    id = 0
    while id < len(text):
        if chunk_num % key_length == 0:
            chunk_num = 0
        matrix[chunk_num].append(text[id])
        chunk_num += 1
        id += 1

    return matrix


def decrypt_phrase(text: bytes, key_length: int) -> str:
    key = get_key_word(text, key_length)
    repeated_key = bytes([ord(key[i % key_length]) for i in range(len(text))])
    decrypted = bytes([byte ^ key_l for key_l, byte in zip(repeated_key, text)])
    return decrypted


if __name__ == '__main__':
    intro_tasks = [
        ("7958401743454e1756174552475256435e59501a5c524e176f786517545e475f524519177219"
         "5019175e4317445f58425b531743565c521756174443455e595017d5b7ab5f525b5b58174058"
         "455b53d5b7aa175659531b17505e41525917435f52175c524e175e4417d5b7ab5c524ed5b7aa"
         "1b174f584517435f5217515e454443175b524343524517d5b7ab5fd5b7aa17405e435f17d5b7"
         "ab5cd5b7aa1b17435f5259174f584517d5b7ab52d5b7aa17405e435f17d5b7ab52d5b7aa1b17"
         "435f525917d5b7ab5bd5b7aa17405e435f17d5b7ab4ed5b7aa1b1756595317435f5259174f58"
         "451759524f4317545f564517d5b7ab5bd5b7aa17405e435f17d5b7ab5cd5b7aa175650565e59"
         "1b17435f525917d5b7ab58d5b7aa17405e435f17d5b7ab52d5b7aa1756595317445817585919"
         "176e5842175a564e17424452175659175e5953524f1758511754585e59545e53525954521b17"
         "7f565a5a5e595017535e4443565954521b177c56445e445c5e17524f565a5e5956435e58591b"
         "17444356435e44435e54565b17435244434417584517405f564352415245175a52435f585317"
         "4e5842175152525b174058425b5317445f584017435f52175552444317455244425b4319"),

        ("G0IFOFVMLRAPI1QJbEQDbFEYOFEPJxAfI10JbEMFIUAAKRAfOVIfOFkYOUQFI15ML1kcJFUeYhA4"
         "IxAeKVQZL1VMOFgJbFMDIUAAKUgFOElMI1ZMOFgFPxADIlVMO1VMO1kAIBAZP1VMI14ANRAZPEAJ"
         "PlMNP1VMIFUYOFUePxxMP19MOFgJbFsJNUMcLVMJbFkfbF8CIElMfgZNbGQDbFcJOBAYJFkfbF8C"
         "KRAeJVcEOBANOUQDIVEYJVMNIFwVbEkDORAbJVwAbEAeI1INLlwVbF4JKVRMOF9MOUMJbEMDIVVM"
         "P18eOBADKhALKV4JOFkPbFEAK18eJUQEIRBEO1gFL1hMO18eJ1UIbEQEKRAOKUMYbFwNP0RMNVUN"
         "PhlAbEMFIUUALUQJKBANIl4JLVwFIldMI0JMK0INKFkJIkRMKFUfL1UCOB5MH1UeJV8ZP1wVYBAbP"
         "lkYKRAFOBAeJVcEOBACI0dAbEkDORAbJVwAbF4JKVRMJURMOF9MKFUPJUAEKUJMOFgJbF4JNERMI"
         "14JbFEfbEcJIFxCbHIJLUJMJV5MIVkCKBxMOFgJPlVLPxACIxAfPFEPKUNCbDoEOEQcPwpDY1QDL"
         "0NCK18DK1wJYlMDIR8II1MZIVUCOB8IYwEkFQcoIB1ZJUQ1CAMvE1cHOVUuOkYuCkA4eHMJL3c8J"
         "WJffHIfDWIAGEA9Y1UIJURTOUMccUMELUIFIlc=")
    ]

    # first line solving:
    # f_decoded = codecs.decode(intro_tasks[0], "hex")
    # decode_single_byte_cipher(f_decoded)

    #  second line solving
    s_decoded = base64.b64decode(intro_tasks[1])

    names, values = get_key_length(s_decoded)

    # plt.figure(figsize=(9, 3))
    # plt.bar(names, values)
    # plt.show()

    #   key length == 3

    print(decrypt_phrase(s_decoded, 3))
