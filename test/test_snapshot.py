# -*- coding: utf-8 -*-

import unittest
import iota
import iotapy


snap = iotapy.snapshot.Snapshot(verify=False)


class SnapshotTest(unittest.TestCase):
    def test_snapshot_init(self):
        self.assertTrue(snap.is_consistent())

    def test_snapshot_diff(self):
        snapshot = iotapy.snapshot.Snapshot(snap.state, 0)
        diff = snapshot.diff(self.get_modified_state(snapshot))
        self.assertEqual(len(diff.keys()), 2)

    def test_snapshot_patch(self):
        snapshot = iotapy.snapshot.Snapshot(snap.state, 0)
        diff = snapshot.diff(self.get_modified_state(snapshot))

        new_state = snapshot.patch(diff, 0)
        diff = snapshot.diff(new_state.state)
        self.assertNotEqual(len(diff), 0)
        self.assertTrue(new_state.is_consistent())

    @unittest.skip('Take too long time to veirfy a snapshot')
    def test_snapshot_init_veirfy(self):
        iotapy.snapshot.Snapshot(verify=True)

    def get_modified_state(self, snapshot):
        h = iota.Hash('PSRQPWWIECDGDDZXHGJNMEVJNSVOSMECPPVRPEVRZFVIZYNNXZNTOTJOZNGCZNQVSPXBXTYUJUOXYASLS')
        m = dict(snapshot.state)

        if m:
            k = next(iter(m))
            m[h] = m[k]
            m[k] = 0

        return m
