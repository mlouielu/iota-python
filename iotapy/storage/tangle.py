# -*- coding: utf-8 -*-

import iota
from iotapy.storage.providers import rocksdb


class Tangle:
    def __init__(self):
        self.provider = rocksdb.RocksDBProvider()
        self.provider.init()

    def get(self, key, column):
        return self.provider.get(key, column)

    def first(self, column):
        return self.provider.first(column)

    def latest(self, column):
        return self.provider.latest(column)
