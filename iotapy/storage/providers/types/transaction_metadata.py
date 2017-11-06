# -*- coding: utf-8 -*-

import struct
import iota
from iotapy.storage import converter as conv


TRANSACTION_METADATA_TRITS_LENGTH = 1604
HASH_BYTES_LENGTH = 49
HASH_TRITS_LENGTH = 243


def get_key(bytes_: bytes):
    # Convert key bytes to iota.TransactionHash
    if not isinstance(bytes_, bytes):
        raise TypeError

    key = iota.TransactionHash.from_trits(conv.from_binary_to_trits(bytes_, HASH_TRITS_LENGTH))
    return key


def get(bytes_: bytes, key=None):
    if bytes_ is None:
        return None
    if not isinstance(bytes_, bytes):
        raise TypeError

    i = 0
    address = iota.Address.from_trits(conv.from_binary_to_trits(bytes_[:HASH_BYTES_LENGTH], HASH_TRITS_LENGTH))
    i += HASH_BYTES_LENGTH
    bundle = iota.BundleHash.from_trits(conv.from_binary_to_trits(bytes_[i:i + HASH_BYTES_LENGTH], HASH_TRITS_LENGTH))
    i += HASH_BYTES_LENGTH
    trunk = iota.TransactionHash.from_trits(conv.from_binary_to_trits(bytes_[i:i + HASH_BYTES_LENGTH], HASH_TRITS_LENGTH))
    i += HASH_BYTES_LENGTH
    branch = iota.TransactionHash.from_trits(conv.from_binary_to_trits(bytes_[i:i + HASH_BYTES_LENGTH], HASH_TRITS_LENGTH))
    i += HASH_BYTES_LENGTH
    legacy_tag = iota.Hash.from_trits(conv.from_binary_to_trits(bytes_[i:i + HASH_BYTES_LENGTH], HASH_TRITS_LENGTH))
    i += HASH_BYTES_LENGTH
    value = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8
    current_index = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8
    last_index = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8
    timestamp = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8

    tag = iota.Hash.from_trits(conv.from_binary_to_trits(bytes_[i:i + HASH_BYTES_LENGTH], HASH_TRITS_LENGTH))
    i += HASH_BYTES_LENGTH
    attachment_timestamp = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8
    attachment_timestamp_lower_bound = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8
    attachment_timestamp_upper_bound = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8

    validity = struct.unpack('>l', bytes_[i:i + 4])[0]
    i += 4
    type_ = struct.unpack('>l', bytes_[i:i + 4])[0]
    i += 4
    arrival_time = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8
    height = struct.unpack('>q', bytes_[i:i + 8])[0]
    i += 8

    # Is confirmed?
    solid = bytes_[i] == 1
    i += 1
    snapshot = struct.unpack('>l', bytes_[i:i + 4])[0]
    i += 4
    sender = bytes_[i:]

    return {
        'address': address,
        'bundle_hash': bundle,
        'trunk_transaction_hash': trunk,
        'branch_transaction_hash': branch,
        'legacy_tag': legacy_tag,
        'value': value,
        'current_index': current_index,
        'last_index': last_index,
        'timestamp': timestamp,
        'tag': tag,
        'attachment_timestamp': attachment_timestamp,
        'attachment_timestamp_lower_bound': attachment_timestamp_lower_bound,
        'attachment_timestamp_upper_bound': attachment_timestamp_upper_bound,
        'validity': validity,
        'type': type_,
        'arrival_time': arrival_time,
        'height': height,
        'solid': solid,
        'snapshot': snapshot,
        'sender': sender
    }


def save(value: iota.Transaction):
    buf = b''

    buf += conv.from_trits_to_binary(value.address.as_trits())
    buf += conv.from_trits_to_binary(value.bundle_hash.as_trits())
    buf += conv.from_trits_to_binary(value.trunk_transaction_hash.as_trits())
    buf += conv.from_trits_to_binary(value.branch_transaction_hash.as_trits())
    buf += conv.from_trits_to_binary(iota.Hash.from_trits(value.legacy_tag.as_trits()).as_trits())
    buf += struct.pack('>q', value.value)
    buf += struct.pack('>q', value.current_index)
    buf += struct.pack('>q', value.last_index)
    buf += struct.pack('>q', value.timestamp)

    buf += conv.from_trits_to_binary(iota.Hash.from_trits(value.tag.as_trits()).as_trits())
    buf += struct.pack('>q', value.attachment_timestamp)
    buf += struct.pack('>q', value.attachment_timestamp_lower_bound)
    buf += struct.pack('>q', value.attachment_timestamp_upper_bound)

    buf += struct.pack('>l', value.validity)
    buf += struct.pack('>l', value.type)
    buf += struct.pack('>q', value.arrival_time)
    buf += struct.pack('>q', value.height)
    buf += struct.pack('>?', value.solid)
    buf += struct.pack('>l', value.snapshot)
    buf += value.sender

    return buf
