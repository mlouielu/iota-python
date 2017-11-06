# -*- coding: utf-8 -*-

import iota
import iotapy
from typing import List


class TransactionRequester:
    def __init__(self, tangle):
        self.tangle = tangle
        self.transactions_to_request = []
        self.milestone_transactions_to_request = []

    def get_requested_transactions(self):
        return self.transactions_to_request + self.milestone_transactions_to_request

    def number_of_transactions_to_request(self):
        return len(self.transactions_to_request) + len(self.milestone_transactions_to_request)

    def clear_transaction_request(self, txh: iota.TransactionHash):
        pass

    def request_transactions(self, txhs: List[iota.TransactionHash], milestone: bool):
        for txh in txhs:
            self.request_transaction(txh, milestone)

    def request_transaction(self, txh: iota.TransactionHash, milestone: bool):
        if txh != EMPTY_HASH and not self.tangle.get(txh, 'transaction'):
            if milestone:
                self.transactions_to_request.remove(txh)
                self.milestone_transactions_to_request.append(txh)
            else:
                if txh not in self.milestone_transactions_to_request:
                    self.transactions_to_request.append(txh)

    def transaction_to_reququest(self, milestone: bool):
        txh = None
        if milestone:
            reqs = self.milestone_transactions_to_request
            if not reqs:
                reqs = self.transactions_to_request
        else:
            reqs = self.transactions_to_request
            if not reqs:
                reqs = self.milestone_transactions_to_request

        while reqs:
            if self.tangle.get(reqs[0], 'transaction'):
                txh = reqs.pop(0)
            else:
                break

        return txh
