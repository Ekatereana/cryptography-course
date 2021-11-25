def single_byte_xor(text: bytes, key: int):
    return bytes([el ^ key for el in text])