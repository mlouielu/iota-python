# -*- coding: utf-8 -*-


class Iota:
    def __init__(self, **kwargs):
        self.configuration = kwargs
        self.testnet = kwargs.get('testnet')
        self.max_peers = kwargs.get('max_peers')
        self.udp_port = kwargs.get('udp_port')
        self.tcp_port = kwargs.get('tcp_port')
