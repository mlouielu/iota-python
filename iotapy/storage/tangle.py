# -*- coding: utf-8 -*-

import iota
from iotapy.storage.providers import rocksdb


class Tangle:
    def __init__(self):
        self.provider = rocksdb.RocksDBProvider()
        self.provider.init()

    def get(self, key, column):
        return self.provider.get(key, column)
