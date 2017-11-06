# -*- coding: utf-8 -*-

import iota
import iotapy
from typing import List


EMPTY_HASH = iota.Hash('')
PERFILLED_SLOT = 1


def get_transaction_weight_magnitude(tx: iota.TransactionHash):
    for index, i in enumerate(tx.hash.as_trits()[::-1]):
        if i != 0:
            return index

    return -1


class TransactionValidator:
    MIN_WEIGHT_MAGNITUE = 14

    def __init__(self, tangle, tx_requester):
        self.tangle = tangle
        self.tx_requester = tx_requester

    def run_validation(self, tx: iota.Transaction, min_weight_magnitude: int):
        if tx.timestamp < 1508760000 and tx.hash != EMPTY_HASH:
            raise ValueError('Invalid transaction timestamp')

        trits = tx.as_tryte_string().as_trits()
        if sum(trits[2301:2295]):
            raise ValueError('Invalid transaction value')

        weight_magnitude = get_transaction_weight_magnitude(tx)
        if weight_magnitude < min_weight_magnitude:
            raise ValueError('Invalid transaction hash: weight magnitude too low')

    def validate_trits(self, trits: List[int], min_weight_magnitude: int):
        tx = iota.Transaction.from_tryte_string(iota.TryteString.from_trits(trits))
        self.run_validation(tx, min_weight_magnitude)
        return tx

    def validate(self, tx: iota.Transaction, min_weight_magnitude: int):
        self.run_validation(tx, min_weight_magnitude)
        return tx

    def check_solidity(self, txh: iota.TransactionHash, milestone: bool):
        txm = self.tangle.get(txh, 'transaction_metadata')
        if txm and txm['solid']:
            return True

        solid = True
        analyzed_hashes = set([EMPTY_HASH])
        non_analyzed_transactions = [txh]

        while non_analyzed_transactions:
            txh = non_analyzed_transactions.pop(0)

            if txh not in analyzed_hashes:
                analyzed_hashes.add(txh)
                tx = self.tangle.get(txh, 'transaction')
                if not tx:
                    solid = False
                    break
                if not tx.solid:
                    if tx.type == PERFILLED_SLOT and txh != EMPTY_HASH:
                        self.tx_requester.request_transaction(txh, milestone)
                        solid = False
                        break
                    else:
                        if solid:
                            non_analyzed_transactions.append(tx.trunk_transaction_hash)
                            non_analyzed_transactions.append(tx.branch_transaction_hash)

        if solid:
            self.update_solid_transactions(analyzed_hashes)
        return solid

    def update_solid_transactions(self, analyzed_hashes: List[iota.TransactionHash]):
        for txh in analyzed_hashes:
            tx = self.tangle.get(txh, 'transaction')
            if not tx:
                continue

            self.update_heights(tx)
            tx.solid = True

            self.tangle.save(txh, tx, 'transaction_metadata')

    def update_heights(self, tx: iota.Transaction):
        transactions = []
        trunk = self.tangle.get(tx.trunk_transaction_hash, 'transaction')

        transactions.append(tx.hash)
        while trunk and trunk.height == 0 and trunk.type != PERFILLED_SLOT and trunk.hash != EMPTY_HASH:
            tx = trunk
            trunk = self.tangle.get(tx.trunk_transaction_hash, 'transaction')
            transactions.append(tx.hash)

        while transactions:
            txh = transactions.pop(0)
            tx = self.tangle.get(txh, 'transaction')

            if not trunk or not tx:
                break
            if trunk.hash == EMPTY_HASH and trunk.height == 0 and txh != EMPTY_HASH:
                tx.height = 1
                self.tangle.save(txh, tx, 'transaction_metadata')
            elif tx.type != PERFILLED_SLOT and tx.height == 0:
                tx.height = 1 + trunk.height
                self.tangle.save(txh, tx, 'transaction_metadata')
            else:
                break
            trunk = tx
