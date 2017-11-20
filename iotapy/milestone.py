# -*- coding: utf-8 -*-

import iota
import iotapy


class Milestone:
    def __init__(self, tangle):
        self.tangle = tangle

    def validate_milestone(self, mode, tx: iota.Transaction):
        if index < 0 or index >= 0x200000:
            return False

        if self.tangle.get(index, 'milestone'):
            return True

        bundle_validator = iota.BundleValidator(self.tangle.get_bundle(tx))
        if len(bundle_validator.bundle) == 0:
            return False



    def get_index(self, tx: iota.Transaction):
        v = 0
        trits = tx.legacy_tag.as_trits()
        for i in range(14, -1, -1):
            v = v * 3 + trits[i]
        return v
