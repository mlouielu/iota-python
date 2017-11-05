
import struct
import iota
from typing import List, Tuple
from iotapy.storage import converter


STATE_DIFF_TRITS_LENGTH = 243
STATE_DIFF_BYTES_LENGTH = 49 + 8


def get_key(bytes_: bytes):
    # Convert key bytes to iota.TransactionHash
    if not isinstance(bytes_, bytes):
        raise TypeError

    key = iota.TransactionHash.from_trits(converter.from_binary_to_trits(bytes_, STATE_DIFF_TRITS_LENGTH))
    return key


def get(bytes_: bytes):
    if bytes_ is None:
        return iter(())
    if not isinstance(bytes_, bytes):
        raise TypeError

    for i in range(0, len(bytes_), STATE_DIFF_BYTES_LENGTH + 1):
        value = struct.unpack('>q', bytes_[i + STATE_DIFF_BYTES_LENGTH - 8:i + STATE_DIFF_BYTES_LENGTH])[0]
        ti = converter.from_binary_to_trits(bytes_[i:i + STATE_DIFF_BYTES_LENGTH - 8], STATE_DIFF_TRITS_LENGTH)

        yield (iota.TransactionHash.from_trits(ti), value)


def save(value: List[Tuple[iota.TransactionHash, int]]):
    if not value:
        return b''

    return b','.join(
        [converter.from_trits_to_binary(i[0].as_trits()) + struct.pack('>q', i[1]) for i in value])
