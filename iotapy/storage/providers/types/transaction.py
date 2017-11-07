# -*- coding: utf-8 -*-

import iota
from iotapy.storage import converter

HASH_TRITS_LENGTH = 243
TRANSACTION_TRITS_LENGTH = 8019


def get_key(bytes_: bytes):
    # Convert key bytes to iota.TransactionHash
    if not isinstance(bytes_, bytes):
        raise TypeError

    key = iota.TransactionHash.from_trits(converter.from_binary_to_trits(bytes_, 243))
    return key


def get(bytes_: bytes, key=None):
    if bytes_ is None:
        return None
    if not isinstance(bytes_, bytes):
        raise TypeError

    ti = converter.from_binary_to_trits(bytes_, TRANSACTION_TRITS_LENGTH)
    return iota.Transaction.from_tryte_string(iota.TryteString.from_trits(ti), key)


def save(value: iota.Transaction):
    if not value:
        return b''

    return converter.from_trits_to_binary(value.as_tryte_string().as_trits())


def store(txh: iota.TransactionHash, tx: iota.Transaction):
    # (key, value, column)
    return [
        (tx.address, [txh], 'address'),
        (tx.bundle_hash, [txh], 'bundle'),
        (tx.branch_transaction_hash, [txh], 'approvee'),
        (tx.trunk_transaction_hash, [txh], 'approvee'),
        (tx.legacy_tag, [txh], 'tag'),
        (txh, tx, 'transaction'),
        (txh, tx, 'transaction_metadata')
    ]


class Transaction(iota.Transaction):
    validity = 0
    type = 1
    arrival_time = 0

    solid = False
    height = 0
    sender = b''
    snapshot = 0

    def set_metadata(self, metadata: dict):
        self.validity = metadata.get('validity', self.validity)
        self.type = metadata.get('type', self.type)
        self.arrival_time = metadata.get('arrival_time', self.arrival_time)
        self.solid = metadata.get('solid', self.solid)
        self.height = metadata.get('height', self.height)
        self.sender = metadata.get('sender', self.sender)
        self.snapshot = metadata.get('snapshot', self.snapshot)
