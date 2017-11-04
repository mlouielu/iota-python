# -*- coding: utf-8 -*-

import functools
import iota

from collections import defaultdict


MAX_VALUE = 2 ** 64 // 2


class TipsManager:
    def __init__(self, tangle, ledger_validator, transaction_validator, max_depth=100):
        self.tangle = tangle
        self.ledger_validator = ledger_validator
        self.transaction_validator = transaction_validator
        self.max_depth = max_depth

    def transaction_to_approve(self,
                               reference: iota.TransactionHash,
                               extra_tip: iota.TransactionHash,
                               depth: int, iterations: int, seed: int):
        ratings = {}
        max_depth_ok = set()
        tip = self.entry_point(reference, extra_tip, depth)
        self.serial_update_ratings(tip, ratings, extra_tip)
        return self.markov_chain_monte_carlo(tip, extra_tip, ratings, iterations,
                                             self.tangle.latest('milestone')[0] - depth * 2,
                                             max_depth_ok, seed)

    def entry_point(self, reference: iota.TransactionHash,
                    extra_tip: iota.TransactionHash,
                    depth: int):
        tip = self.tangle.latest('milestone')[1][1] if not reference else reference
        if extra_tip:
           pass

        return tip
    
    def markov_chain_monte_carlo(self, tip: iota.TransactionHash,
                                 extra_tip: iota.TransactionHash,
                                 ratings: dict,
                                 iterations: int,
                                 max_depth: int,
                                 max_depth_ok: dict,
                                 seed: int):
        monte_carlo_integrations = defaultdict(int)

        for _ in range(iterations):
            tail = self.random_walk(tip, extra_tip, ratings, max_depth,
                                    max_depth_ok, seed)
            monte_carlo_integrations[tail] += 1

        # XXX: Remember todo random
        return functools.reduce(
            lambda x, y: max(monte_carlo_integrations[x],
                             monte_carlo_integrations[y]),
            monte_carlo_integrations, None)

    def random_walk(self, start: iota.TransactionHash,
                    extra_tip: iota.TransactionHash,
                    ratings: dict,
                    max_depth: int,
                    max_depth_ok: dict,
                    rnd: int):
        tip = start
        tail = tip
        analyzed_tips = set()
        traversed_tails = 0

        while tip:
            tx = self.tangle.get(tip, 'transaction')
            approvers = self.tangle.get(tip, 'approvee')
            approvers = list(approvers) if approvers else []
    
            if tx.current_index == 0:
                # bla bla bla check
                tail = tip
                traversed_tails += 1

            if not approvers:
                break
            elif len(approvers) == 1:
                # next hash
                pass
            else:
                # Walk to the next approver
                if tip not in ratings:
                    self.serial_update_ratings(tip, ratings, extra_tip)

                walk_ratings = [0.0] * len(approvers)
                max_rating = 0.0
                for i, t in enumerate(approvers):
                    if t in ratings:
                        walk_ratings[i] = ratings[t] ** .5
                        max_rating += walk_ratings[i]
                rating_weight = 500  # XXX: randomize
                for index, i in enumerate(walk_ratings[::-1]):
                    rating_weight -= i
                    if rating_weight < 1:
                        break

                tip = approvers[i]
                if tx == tip:
                    break

        return tail
        
    def serial_update_ratings(self,
                              txh: iota.TransactionHash,
                              ratings: dict,
                              extra_tip: iota.TransactionHash):
        analyzed_tips = set()
        hashes_to_rate = []  # As a stack
        hashes_to_rate.append(txh)

        while hashes_to_rate:
            current_hash = hashes_to_rate.pop()
            added_back = False
            approvers = self.tangle.get(current_hash, 'approvee')
            approvers = approvers if approvers else []

            for approver in approvers:
                if ratings.get(approver) and approver != current_hash:
                    if not added_back:
                        added_back = True
                        hashes_to_rate.append(current_hash)
                    hashes_to_rate.append(approver)

            if not added_back and current_hash not in analyzed_tips:
                analyzed_tips.add(current_hash)
                rating = 1 if extra_tip and self.ledger_validator.is_approved(current_hash) else 0
                rating += functools.reduce(
                    lambda a, b: MAX_VALUE if a + b < 0 or a + b > MAX_VALUE else a + b,
                    filter(lambda x: x, map(ratings.get, approvers)), 0)
                ratings[current_hash] = rating
