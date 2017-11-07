"""A Pure-Python implementation of IOTA node"""

import iota
import iotapy.network
import iotapy.snapshot
import iotapy.storage

__version__ = '0.1.2'


# Monkey patch iota.Transaction to handle metadata
iota.Transaction = iotapy.storage.providers.types.transaction.Transaction
