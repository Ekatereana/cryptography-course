from operator import itemgetter

TRAIN_TEXT = '../assets/train_text.txt'


def decrypt_text(encrypted_text: []) -> str:
    dictionary = create_dict(encrypted_text)
    decrypted_list = []

    for letter in encrypted_text:
        ascii_code = ord(letter)
        if 65 <= ascii_code <= 90:
            decrypted_list.append(dictionary[letter])

    decrypted_text = "".join(decrypted_list)

    return decrypted_text


def create_dict(text: []) -> {}:
    plain_text = read_file(TRAIN_TEXT)

    plain_frequencies = count_letter_frequencies(plain_text)
    encrypted_frequencies = count_letter_frequencies(text)

    decryption_dict = {}
    for i in range(0, len(encrypted_frequencies)):
        decryption_dict[encrypted_frequencies[i][0]] = plain_frequencies[i][0]
    return decryption_dict


def count_letter_frequencies(text):
    frequencies = {}

    for letter in text:
        ascii_code = ord(letter)
        if 65 >= ascii_code <= 90:
            frequencies[chr(ascii_code)] = 0
        if chr(ascii_code) not in frequencies.keys():
            frequencies[chr(ascii_code)] = 0
        else:
            frequencies[chr(ascii_code)] += 1

    sorted_by_frequency = sorted(frequencies.items(), key=itemgetter(1), reverse=True)

    return sorted_by_frequency


def read_file(path):
    f = open(path, "r")
    text = f.read().replace(" ", "").upper()
    f.close()
    return text
