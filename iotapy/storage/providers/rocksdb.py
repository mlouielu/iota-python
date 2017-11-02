# -*- coding: utf-8 -*-

import struct
import iota
import rocksdb_iota
import iotapy.storage.providers.types
from rocksdb_iota.merge_operators import StringAppendOperator
from iotapy.storage import converter


KB = 1024
MB = KB * 1024


class RocksDBProvider:
    BLOOM_FILTER_BITS_PER_KEY = 10
    column_family_names = [
        b'default',
        b'transaction',
        b'transaction-metadata',
        b'milestone',
        b'stateDiff',
        b'address',
        b'approvee',
        b'bundle',
        b'tag'
    ]

    column_family_python_mapping = {
        'transaction_metadata': 'transaction-metadata',
        'state_diff': 'stateDiff'
    }

    def __init__(self, db_path, db_log_path, cache_size=4096, read_only=True):
        self.db = None
        self.db_path = db_path
        self.db_log_path = db_log_path
        self.cache_size = cache_size
        self.read_only = read_only
        self.available = False

    def init(self):
        self.init_db(self.db_path, self.db_log_path)
        self.available = True

    def init_db(self, db_path, db_log_path):
        options = rocksdb_iota.Options(
            create_if_missing=True,
            db_log_dir=db_log_path,
            max_log_file_size=MB,
            max_manifest_file_size=MB,
            max_open_files=10000,
            max_background_compactions=1
        )

        options.allow_concurrent_memtable_write = True

        # XXX: How to use this?
        block_based_table_config = rocksdb_iota.BlockBasedTableFactory(
            filter_policy=rocksdb_iota.BloomFilterPolicy(self.BLOOM_FILTER_BITS_PER_KEY),
            block_size_deviation=10,
            block_restart_interval=16,
            block_cache=rocksdb_iota.LRUCache(self.cache_size * KB),
            block_cache_compressed=rocksdb_iota.LRUCache(32 * KB, shard_bits=10))
        options.table_factory = block_based_table_config

        # XXX: How to use this?
        column_family_options = rocksdb_iota.ColumnFamilyOptions(
            merge_operator=StringAppendOperator(),
            table_factory=block_based_table_config,
            max_write_buffer_number=2,
            write_buffer_size=2 * MB)

        self.db = rocksdb_iota.DB(self.db_path, options, self.column_family_names,
                                  read_only=self.read_only)

    def _convert_column_to_handler(self, column):
        if not isinstance(column, str):
            raise TypeError('Column type should be str')

        db_column = self.column_family_python_mapping.get(column, column)
        ch = self.db.column_family_handles.get(bytes(db_column, 'ascii'))
        if ch is None:
            raise KeyError('Invalid column family name: %s' % (column))

        return ch

    def _convert_key_column(self, key, column):
        # Convert column to column family handler
        ch = self._convert_column_to_handler(column)

        # Expand iota.Tag to iota.Hash
        if column == 'tag':
            if not isinstance(key, iota.Tag):
                raise TypeError('Tag key type should be iota.Tag')
            key = iota.Hash(str(key))

        # Convert key into trits-binary
        if column == 'milestone':
            if not isinstance(key, int):
                raise TypeError('Milestone key type should be int')
            key = struct.pack('>l', key)
        else:
            if not isinstance(key, iota.TryteString):
                raise TypeError('Key type should be iota.TryteString')
            if len(key) != iota.Hash.LEN:
                raise ValueError('Key length must be 81 trytes')
            key = converter.from_trits_to_binary(key.as_trits())

        return key, ch

    def _get(self, bytes_, column):
        # Convert value (bytes_) into data object
        return getattr(iotapy.storage.providers.types, column).get(bytes_)

    def _get_key(self, bytes_, column):
        return getattr(iotapy.storage.providers.types, column).get_key(bytes_)

    def get(self, key, column):
        key, ch = self._convert_key_column(key, column)

        # Get binary data from database
        bytes_ = self.db.get(key, ch)
        if not bytes_:
            return None

        return self._get(bytes_, column)

    def next(self, key, column):
        key, ch = self._convert_key_column(key, column)

        it = self.db.iteritems(ch)
        it.seek(key)
        next(it)

        # XXX: We will get segfault if this is NULL in database
        key, bytes_ = it.get()
        if not bytes_:
            return None

        # Convert into data object
        return self._get_key(key, column), self._get(bytes_, column)

    def first(self, column):
        ch = self._convert_column_to_handler(column)

        it = self.db.iteritems(ch)
        it.seek_to_first()

        # XXX: We will get segfault if this is NULL in database
        key, bytes_ = it.get()
        if not bytes_:
            return None

        # Convert into data object
        return self._get_key(key, column), self._get(bytes_, column)

    def latest(self, column):
        ch = self._convert_column_to_handler(column)

        it = self.db.iteritems(ch)
        it.seek_to_last()

        # XXX: We will get segfault if this is NULL in database
        key, bytes_ = it.get()
        if not bytes_:
            return None

        # Convert into data object
        return self._get_key(key, column), self._get(bytes_, column)

    def may_exist(self, key, column, fetch=False):
        key, ch = self._convert_key_column(key, column)

        # XXX: Not working......
        return self.db.key_may_exist(key, ch)[0]
