alphabet_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def fitness_func(text: bytes, chromosome: bytes, pivot: int):
    source_grams = calculate_n_grams(text, pivot)


def calculate_n_grams(text: bytes, pivot: int) -> []:
    n_grams = []
    for i in range(len(text) - pivot):
        n_grams.append(text[i:i + pivot])

    return n_grams


def calc_fq(text: bytes, n_gram: bytes) -> int:
    fq = 0
    for group in text:
        if group == n_gram:
            fq += 1
    return fq


def decrypt_with_key(text: bytes, key: bytes) -> bytes:
    decrypted = b''
    for byte in text:
        id = alphabet_order.index(byte)
        decrypted += key[id]
    return decrypted


if __name__ == '__main__':
    intro_tasks = [
        ("EFFPQLEKVTVPCPYFLMVHQLUEWCNVWFYGHYTCETHQEKLPVMSAKSPVPAPV"
         "YWMVHQLUSPQLYWLASLFVWPQLMVHQLUPLRPSQLULQESPBLWPCSVRVWFLHL"
         "WFLWPUEWFYOTCMQYSLWOYWYETHQEKLPVMSAKSPVPAPVYWHEPPLUWSGYUL"
         "EMQTLPPLUGUYOLWDTVSQETHQEKLPVPVSMTLEUPQEPCYAMEWWYTYWDLUUL"
         "TCYWPQLSEOLSVOHTLUYAPVWLYGDALSSVWDPQLNLCKCLRQEASPVILSLEUM"
         "QBQVMQCYAHUYKEKTCASLFPYFLMVHQLUPQLHULIVYASHEUEDUEHQBVTTPQ"
         "LVWFLRYGMYVWMVFLWMLSPVTTBYUNESESADDLSPVYWCYAMEWPUCPYFVIVF"
         "LPQLOLSSEDLVWHEUPSKCPQLWAOKLUYGMQEUEMPLUSVWENLCEWFEHHTCGU"
         "LXALWMCEWETCSVSPYLEMQYGPQLOMEWCYAGVWFEBECPYASLQVDQLUYUFLU"
         "GULXALWMCSPEPVSPVMSBVPQPQVSPCHLYGMVHQLUPQLWLRPOEDVMETBYUF"
         "BVTTPENLPYPQLWLRPTEKLWZYCKVPTCSTESQPBYMEHVPETCMEHVPETZMEH"
         "VPETKTMEHVPETCMEHVPETT")
    ]

    # third line solving:
    print(calculate_n_grams(bytes(intro_tasks[0], "ascii"), 3))
