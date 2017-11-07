# -*- coding: utf-8 -*-

import random
import iota


def get_random_trits(length):
    return [random.randint(-1, 1) for _ in range(length)]


def get_random_hash():
    return iota.Hash.from_trits(get_random_trits(243))


def get_random_transaction_hash():
    return iota.TransactionHash.from_trits(get_random_trits(243))


def get_random_transaction():
    return iota.Transaction.from_tryte_string(
        iota.TryteString.from_trits(get_random_trits(8019)),
        get_random_transaction_hash())


def get_random_transaction_with_trunk_and_branch(trunk, branch):
    tx = get_random_transaction()
    tx.trunk_transaction_hash = trunk
    tx.branch_transaction_hash = branch

    return tx
