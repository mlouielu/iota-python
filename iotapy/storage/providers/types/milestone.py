# -*- coding: utf-8 -*-

import struct
import iota
from typing import Tuple
from iotapy.storage import converter


HASH_TRITS_LENGTH = 243


def get_key(bytes_: bytes):
    # Convert key bytes to key object
    if not isinstance(bytes_, bytes):
        raise TypeError

    key = struct.unpack('>l', bytes_)[0]
    return key


def get(bytes_: bytes, key=None):
    if bytes_ is None:
        return None
    if not isinstance(bytes_, bytes):
        raise TypeError

    index = struct.unpack('>l', bytes_[:4])[0]
    milestone = iota.TransactionHash.from_trits(
        converter.from_binary_to_trits(bytes_[4:], HASH_TRITS_LENGTH))

    return (index, milestone)


def save(value: Tuple[int, iota.TransactionHash]):
    if not value:
        return b''

    return struct.pack('>l', value[0]) + converter.from_trits_to_binary(value[1].as_trits())
