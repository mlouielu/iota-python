# -*- coding: utf-8 -*-

import tempfile
import unittest
import iota
import iotapy
from iotapy.storage.providers import rocksdb
from test import utils


class TipsManagerTest(unittest.TestCase):
    def setUp(self):
        self.db_path = tempfile.mkdtemp()
        self.db_log_path = tempfile.mkdtemp()

        self.provider = rocksdb.RocksDBProvider(self.db_path, self.db_log_path, read_only=False)
        self.provider.init()

        self.tips = iotapy.tips.TipsManager(self.provider, None, None)

    def cleanUp(self):
        del self.provider.db
        del self.provider
        shutil.rmtree(self.db_path)
        shutil.rmtree(self.db_log_path)

    def test_update_linear_ratings_3_should_work(self):
        tx = utils.get_random_transaction()
        tx1 = utils.get_random_transaction_with_trunk_and_branch(tx.hash, tx.hash)
        tx2 = utils.get_random_transaction_with_trunk_and_branch(tx1.hash, tx1.hash)

        self.provider.store(tx.hash, tx, 'transaction')
        self.provider.store(tx1.hash, tx1, 'transaction')
        self.provider.store(tx2.hash, tx2, 'transaction')

        ratings = {}
        self.tips.update_hash_ratings(tx.hash, ratings, set())

        self.assertEqual(len(ratings[tx.hash]), 3)
        self.assertEqual(len(ratings[tx1.hash]), 2)
        self.assertEqual(len(ratings[tx2.hash]), 1)

    def test_update_linear_ratings_5_should_work(self):
        tx = utils.get_random_transaction()
        tx1 = utils.get_random_transaction_with_trunk_and_branch(tx.hash, tx.hash)
        tx2 = utils.get_random_transaction_with_trunk_and_branch(tx1.hash, tx1.hash)
        tx3 = utils.get_random_transaction_with_trunk_and_branch(tx2.hash, tx2.hash)
        tx4 = utils.get_random_transaction_with_trunk_and_branch(tx3.hash, tx3.hash)

        self.provider.store(tx.hash, tx, 'transaction')
        self.provider.store(tx1.hash, tx1, 'transaction')
        self.provider.store(tx2.hash, tx2, 'transaction')
        self.provider.store(tx3.hash, tx3, 'transaction')
        self.provider.store(tx4.hash, tx4, 'transaction')

        ratings = {}
        self.tips.update_hash_ratings(tx.hash, ratings, set())

        self.assertEqual(len(ratings[tx.hash]), 5)
        self.assertEqual(len(ratings[tx1.hash]), 4)
        self.assertEqual(len(ratings[tx2.hash]), 3)

    def test_recursive_update_ratings_5_should_work(self):
        tx = utils.get_random_transaction()
        tx1 = utils.get_random_transaction_with_trunk_and_branch(tx.hash, tx.hash)
        tx2 = utils.get_random_transaction_with_trunk_and_branch(tx1.hash, tx1.hash)
        tx3 = utils.get_random_transaction_with_trunk_and_branch(tx2.hash, tx2.hash)
        tx4 = utils.get_random_transaction_with_trunk_and_branch(tx3.hash, tx3.hash)

        self.provider.store(tx.hash, tx, 'transaction')
        self.provider.store(tx1.hash, tx1, 'transaction')
        self.provider.store(tx2.hash, tx2, 'transaction')
        self.provider.store(tx3.hash, tx3, 'transaction')
        self.provider.store(tx4.hash, tx4, 'transaction')

        ratings = {}
        self.tips.recursive_update_ratings(tx.hash, ratings, set())
        self.assertEqual(ratings[tx.hash], 5)

    def test_recursive_update_ratings_with_different_tb_should_work(self):
        txs = [utils.get_random_transaction()]
        self.provider.store(txs[0].hash, txs[0], 'transaction')

        for i in range(1, 5):
            txs.append(utils.get_random_transaction_with_trunk_and_branch(
                txs[i - 1].hash, txs[i - (2 if i > 1 else 1)].hash))
            self.provider.store(txs[-1].hash, txs[-1], 'transaction')

        ratings = {}
        self.tips.recursive_update_ratings(txs[0].hash, ratings, set())
        self.assertEqual(ratings[txs[0].hash], 12)
