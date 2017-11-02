# -*- coding: utf-8 -*-

import iota
from iotapy.storage import converter


HASH_TRITS_LENGTH = 243
HASH_BYTES_LENGTH = 49


def get_key(bytes_: bytes):
    # Convert key bytes to iota.TransactionHash
    if not isinstance(bytes_, bytes):
        raise TypeError

    key = iota.TransactionHash.from_trits(converter.from_binary_to_trits(bytes_, HASH_TRITS_LENGTH))
    return key


def get(bytes_: bytes):
    if not isinstance(bytes_, bytes):
        raise TypeError

    for i in range(0, len(bytes_), HASH_BYTES_LENGTH + 1):
        ti = converter.from_binary_to_trits(bytes_[i:i + HASH_BYTES_LENGTH], HASH_TRITS_LENGTH)
        yield iota.types.TransactionHash.from_trits(ti)
