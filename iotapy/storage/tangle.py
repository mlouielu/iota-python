# -*- coding: utf-8 -*-

import iota
from iotapy.storage.providers import rocksdb


class Tangle:
    def __init__(self, provider):
        self.provider = provider
        self.provider.init()

    def get(self, key, column):
        return self.provider.get(key, column)

    def first(self, column):
        return self.provider.first(column)

    def latest(self, column):
        return self.provider.latest(column)

    def save(self, key, value, column):
        return self.provider.save(key, value, column)

    def store(self, key, value, column):
        self.provider.store(key, value, column)

    def _traverse_bundle(self, tx: iota.Transaction, target: iota.TransactionHash = None):
        if not target and tx.current_index:
            raise ValueError('Traverse start with non-tail transaction')

        if target:
            if target != tx.bundle_hash:
                # We've hit a different bundle, stop now
                return []
        else:
            target = tx.bundle_hash

        if tx.current_index == tx.last_index == 0:
            # Bundle only has one transaction
            return [tx]

        # Recursively follow the trunk transacion, to fetch the next
        # transaction in the bundle
        return [tx] + self._traverse_bundle(
            tx.trunk_transaction_hash, target)

    def get_bundle(self, tx: iota.Transaction):
        return self._traverse_bundle(tx)
