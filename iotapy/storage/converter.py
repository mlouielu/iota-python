# -*- coding: utf-8 -*-

RADIX = 3
BYTE_RADIX = 256
MAX_TRIT_VALUE = (RADIX - 1) // 2
MIN_TRIT_VALUE = -MAX_TRIT_VALUE

NUMBER_OF_TRITS_IN_A_BYTE = 5
NUMBER_OF_TRITS_IN_A_TRYTE = 3

HASH_LENGTH = 243
BYTE_TO_TRITS_MAPPINGS = [[]] * HASH_LENGTH
TRYTE_TO_TRITS_MAPPINGS = [[]] * 27

HIGH_INTEGER_BITS = 0xFFFFFFFF
HIGH_LONG_BITS = 0xFFFFFFFFFFFFFFFF

TRYTE_ALPHABET = '9ABCDEFGHIJKLMNOPQRSTUVWXYZ'

MIN_TRYTE_VALUE = -13
MAX_TRYTE_VALUE = 13


def increment(trits, length):
    for i in range(length):
        trits[i] += 1
        if trits[i] > MAX_TRIT_VALUE:
            trits[i] = MIN_TRIT_VALUE
        else:
            break


def init_converter():
    global BYTE_TO_TRITS_MAPPINGS, TRYTE_TO_TRITS_MAPPINGS

    trits = [0] * NUMBER_OF_TRITS_IN_A_BYTE
    for i in range(HASH_LENGTH):
        BYTE_TO_TRITS_MAPPINGS[i] = trits[:NUMBER_OF_TRITS_IN_A_BYTE]
        increment(trits, NUMBER_OF_TRITS_IN_A_BYTE)

    for i in range(27):
        TRYTE_TO_TRITS_MAPPINGS[i] = trits[:NUMBER_OF_TRITS_IN_A_TRYTE]
        increment(trits, NUMBER_OF_TRITS_IN_A_TRYTE)


def from_trits_to_binary(trits, offset=0, size=HASH_LENGTH):
    b = bytearray(b' ' * int((size + NUMBER_OF_TRITS_IN_A_BYTE - 1) / NUMBER_OF_TRITS_IN_A_BYTE))
    for i in range(len(b)):
        value = 0
        for j in range(size - i * NUMBER_OF_TRITS_IN_A_BYTE - 1 if (size - i * NUMBER_OF_TRITS_IN_A_BYTE) < NUMBER_OF_TRITS_IN_A_BYTE else 4, -1, -1):
            value = value * RADIX + trits[offset + i * NUMBER_OF_TRITS_IN_A_BYTE + j]
        b[i] = value % 256
    return bytes(b)


def from_binary_to_trits(bs, length):
    offset = 0
    trits = [0] * length
    for i in range(min(len(bs), length)):
        # We must convert the binary data
        # because java using different range with Python
        index = bs[i] if bs[i] < 127 else bs[i] - 256 + HASH_LENGTH
        copy_len = length - offset if length - offset < NUMBER_OF_TRITS_IN_A_BYTE else NUMBER_OF_TRITS_IN_A_BYTE
        trits[offset: offset + copy_len] = BYTE_TO_TRITS_MAPPINGS[index][:copy_len]
        offset += NUMBER_OF_TRITS_IN_A_BYTE

    return trits


init_converter()
