import re
import codecs

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
eng_letters = list([l.encode("ascii") for l in dict_eng_fq.keys()])


# solve single byte XOR cipher

def decode_single_byte_cipher(text: bytes):
    for k in range(255):
        try:
            print(single_byte_xor(text, k).decode("utf-8"))
        except UnicodeDecodeError:
            continue


def single_byte_xor(text: bytes, key: int):
    return bytes([el ^ key for el in text])


def get_key_length(text):
    encoded = text.lower().encode("ascii")
    print(encoded)
    for shift in range(1, len(text) - 1):
        print(id_of_coincidence(shift_text(encoded, shift)))


def shift_text(text, shift):
    return str([i for i in text[::shift]])


def id_of_coincidence(origin):
    return sum([fq * (fq - 1)
                for fq in
                [get_fq_letter(l, origin) for l in eng_letters]
                ]
               ) / (len(origin) * (len(origin) - 1))


def get_fq_letter(letter, text):
    amount = re.findall(letter, text)
    return amount / len(text)


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
         "4e5842175152525b174058425b5317445f584017435f52175552444317455244425b4319")
    ]

    # first line solving:
    f_decoded = codecs.decode(intro_tasks[0], "hex")
    decode_single_byte_cipher(f_decoded)
