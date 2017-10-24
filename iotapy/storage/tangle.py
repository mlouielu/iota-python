# -*- coding: utf-8 -*-

import rocksdb
from rocksdb.merge_operators import StringAppendOperator

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

    def __init__(self,
                 db_path='/mainnetdb',
                 db_log_path='/mainnetdb.log', cache_size=4096):
        self.db = None
        self.db_path = db_path
        self.db_log_path = db_log_path
        self.cache_size = cache_size
        self.available = False


    def init(self):
        self.init_db(self.db_path, self.db_log_path);
        self.init_cf_handler()
        self.available = True

    def init_db(self, db_path, db_log_path):
        options = rocksdb.Options(
            create_if_missing=True,
            db_log_dir=db_log_path,
            max_log_file_size=MB,
            max_manifest_file_size=MB,
            max_open_files=10000,
            max_background_compactions=1
        )

        options.allow_concurrent_memtable_write = True

        # XXX: How to use this?
        block_based_table_config = rocksdb.BlockBasedTableFactory(
            filter_policy=rocksdb.BloomFilterPolicy(self.BLOOM_FILTER_BITS_PER_KEY),
            block_size_deviation=10,
            block_restart_interval=16,
            block_cache=rocksdb.LRUCache(self.cache_size * KB),
            block_cache_compressed=rocksdb.LRUCache(32 * KB, shard_bits=10))
        options.table_factory = block_based_table_config

        # XXX: How to use this?
        column_family_options = rocksdb.ColumnFamilyOptions(
            merge_operator=StringAppendOperator(),
            table_format_config=block_based_table_config,
            max_write_buffer_number=2,
            write_buffer_size=2 * MB)

        self.db = rocksdb.DB(self.db_path, options, self.column_family_names)


    def init_cf_handler(self):
        pass


class Tangle:
    def __init__(self):
        self.provider = RocksDBProvider()
        self.provider.init()


if __name__ == '__main__':
    t = Tangle()

    for cfn in t.provider.db.column_family_handles:
        cf = t.provider.db.column_family_handles[cfn]
        it = t.provider.db.iteritems(cf)
        it.seek_to_last()
        print(list(it))
