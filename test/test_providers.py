# -*- coding: utf-8 -*-

import unittest
import iota
import iotapy
from iota import TransactionHash
from iotapy.storage.providers import rocksdb


class RocksDBProviderTest(unittest.TestCase):
    def setUp(self):
        self.provider = rocksdb.RocksDBProvider('/var/db/iota/mainnetdb', '/var/db/iota/mainnetdb.log', read_only=True)
        self.provider.init()

    def tearDown(self):
        del self.provider.db
        del self.provider

    def test_get_tag(self):
        key = iota.Tag(b'EXAMPLEPYTHONLIB')
        value = list(self.provider.get(key, 'tag'))
        expect = [
            TransactionHash(b'GTXDTJVUTVSNHYFPJUOWFKTGQTCMNKZPJDJXSWVQWTXYRDZAVZTX9KFBRIMRQEQLMCMVAUKMZWMHA9999'),
            TransactionHash(b'PZYRMRVTSPQXNEQIQEBAGINMDAKOHPOLNH9LR9DTFWMWFQICXL9BJCWBUPMKZERKYKBDRIBYEJYH99999'),
            TransactionHash(b'UNUK99RCIWLUQ9WMUT9MPQSZCHTUMGN9IWOCOXWMNPICCCQKLLNIIE9UIFGKZLHRI9QAOEQXQJLL99999')
        ]

        self.assertListEqual(value, expect)

        # Bad
        with self.assertRaises(TypeError):
            self.assertIsNone(self.provider.get(iota.TryteString('FOOBAR'), 'tag'))
        with self.assertRaises(TypeError):
            self.provider.get('', 'tag')


    def test_get_transaction(self):
        key = iota.TransactionHash('PZYRMRVTSPQXNEQIQEBAGINMDAKOHPOLNH9LR9DTFWMWFQICXL9BJCWBUPMKZERKYKBDRIBYEJYH99999')
        value = self.provider.get(key, 'transaction')

        # XXX: Skip the test now
        value.as_json_compatible()

    def test_get_transaction_metadata(self):
        key = iota.TransactionHash('PZYRMRVTSPQXNEQIQEBAGINMDAKOHPOLNH9LR9DTFWMWFQICXL9BJCWBUPMKZERKYKBDRIBYEJYH99999')
        value = self.provider.get(key, 'transaction_metadata')
        expect = {'address': iota.Address(b'9TPHVCFLAZTZSDUWFBLCJOZICJKKPVDMAASWJZNFFBKRDDTEOUJHR9JVGTJNI9IYNVISZVXARWJFKUZWC'),
                  'bundle_hash': iota.BundleHash(b'VLQUIJHXNWAINTXQNEQHNIASGSPYPOTNMQCM9RJPETERGLWIIKRLBZSCGPDYSFNZQ9FT9ZMQXZXNITRAC'),
                  'trunk_transaction_hash': TransactionHash(b'KTTHXMASNRQOSGZOW9ODAOBQFXKMPKNKWLIWDBVWJGMKQUBBPX9WHCYXCWEAHVTNZHPDKUWHOWN9Z9999'),
                  'branch_transaction_hash': TransactionHash(b'J9ZMRIJXZOZRNDHKOUBQGHPAPHQ9QOXFEEVQMJBMBOHKEVNUHJTEMRD9W9UDYMTGQ9ENQKDTJMJN99999'),
                  'legacy_tag': iota.Hash(b'EXAMPLEPYTHONLIB99999999999999999999999999999999999999999999999999999999999999999'),
                  'value': 0,
                  'current_index': 0,
                  'last_index': 0,
                  'timestamp': 1508993982,
                  'tag': iota.Hash(b'EXAMPLEPYTHONLIB99999999999999999999999999999999999999999999999999999999999999999'),
                  'attachment_timestamp': 1508993991533,
                  'attachment_timestamp_lower_bound': 0,
                  'attachment_timestamp_upper_bound': 12,
                  'validity': 1,
                  'type': -1,
                  'arrival_time': 1508993991,
                  'height': 0,
                  'solid': True,
                  'snapshot': 251623,
                  'sender': 'local'}

        self.assertIsInstance(value, dict)
        self.assertEqual(value['solid'], True)
        self.assertEqual(value, expect)

    def test_get_milestone(self):
        key = 259773
        value = self.provider.get(key, 'milestone')

        self.assertEqual(value, (259773, iota.TransactionHash(b'9FRPRZZYOQSGZILXVNTSLKULYBODWKWTZHGGZ9WPOCRSJXSLAPNAHENFJNOEKCAMNQPBRNZDVJDZZ9999')))

        # Bad
        self.assertIsNone(self.provider.get(-1, 'milestone'))
        self.assertIsNone(self.provider.get(0, 'milestone'))
        with self.assertRaises(TypeError):
            self.provider.get('test', 'milestone')
        with self.assertRaises(TypeError):
            self.provider.get(b'test', 'milestone')
        with self.assertRaises(TypeError):
            self.provider.get(None, 'milestone')

    def test_get_approvee(self):
        key = iota.TransactionHash(b'UNUK99RCIWLUQ9WMUT9MPQSZCHTUMGN9IWOCOXWMNPICCCQKLLNIIE9UIFGKZLHRI9QAOEQXQJLL99999')
        value = list(self.provider.get(key, 'approvee'))
        expect = [
            TransactionHash(b'YUPJOZMOSVIEQZXSVTLSYMIGMLFGDBPSZUTRAML9MIQNCLCMPOGFRAYLSFJUDBJBFDGESTIAFGZR99999'),
            TransactionHash(b'ELIWEYAYXYEFOWBHJMELTKVERQWTJF9RXRLISNNQQVWGS9EMYYBVWRJYVJUYAPBGDQNYQEZOPBXWA9999'),
        ]

        self.assertListEqual(value, expect)

        # Bad
        self.assertIsNone(self.provider.get(iota.TryteString('9' * (iota.Hash.LEN - 1) + 'A'), 'approvee'))
        self.assertIsNone(self.provider.get(iota.TransactionHash('FOOBAR'), 'approvee'))
        with self.assertRaises(ValueError):
            self.assertIsNone(self.provider.get(iota.TryteString('FOOBAR'), 'approvee'))
        with self.assertRaises(TypeError):
            self.provider.get('', 'approvee')

    def test_get_bundle(self):
        key = iota.BundleHash(b'9ZMDWNXOJUEQQGBFHFPLIXLFBVFP9QIEJQGCD9B9NOAWBHHTCUDECJ9LSDUVP9YBIZGAKHANXBYQTADEZ')
        value = list(self.provider.get(key, 'bundle'))
        expect = [
            TransactionHash(b'9KTTGBWZWKMGY9OTVFCRKUJTMOSRPNDDYKSWJENSH9MBQU9VKLVCWQPPULJHAYYM9JEMTYDTNTI9Z9999'),
            TransactionHash(b'HDLRDWIYLHDEOXEMCIVQOOLOGFEBUDHTRRDRLLDIYQUFPSNCUYRQBRUPB9DWLQWCBYVXTBFYFPYGZ9999'),
            TransactionHash(b'INLMRLGUURIAVIKCBUCBNEALFLVHFRGWPKUBBEFKOMFRROCSDGXSTWXRBHOXERJKDCURA9LJUHIN99999')
        ]

        self.assertListEqual(value, expect)

        # Bad
        self.assertIsNone(self.provider.get(iota.TryteString('9' * (iota.Hash.LEN - 1) + 'A'), 'bundle'))
        self.assertIsNone(self.provider.get(iota.BundleHash('FOOBAR'), 'bundle'))
        with self.assertRaises(ValueError):
            self.assertIsNone(self.provider.get(iota.TryteString('FOOBAR'), 'bundle'))
        with self.assertRaises(TypeError):
            self.provider.get('', 'bundle')

    def test_get_address(self):
        key = iota.Address(b'9TPHVCFLAZTZSDUWFBLCJOZICJKKPVDMAASWJZNFFBKRDDTEOUJHR9JVGTJNI9IYNVISZVXARWJFKUZWC')
        value = list(self.provider.get(key, 'address'))

        self.assertGreaterEqual(len(value), 86)
        self.assertIsInstance(value[0], iota.TransactionHash)

        # Bad
        self.assertIsNone(self.provider.get(iota.TryteString('9' * (iota.Hash.LEN - 1) + 'A'), 'address'))
        self.assertIsNone(self.provider.get(iota.Address('FOOBAR'), 'address'))
        with self.assertRaises(ValueError):
            self.assertIsNone(self.provider.get(iota.TryteString('FOOBAR'), 'address'))
        with self.assertRaises(TypeError):
            self.provider.get('', 'address')

    def test_get_state_diff(self):
        key = iota.TransactionHash(b'ZRWRRONUH9RRGUWSCF9GFZVOLDQRHEYLLTK9AKRALNZPMHY9ZEXELICWGFFJTRMDUEYEVDSLCWKSZ9999')
        value = list(self.provider.get(key, 'state_diff'))
        expect = [
            (TransactionHash(b'ETOTZUWBFOIXGWLVAWLQDRX9PV9ADSURFKAPMGSKUXVOBFDEAGTYPNAKQMMIRYJAQIGJNHTJJAXORXIBC'), 15000000),
            (TransactionHash(b'ITO9RDEJSMVTALFNCKDHNMOLXK9VMNXHKYQHJFZSZVBICBETUTKYKFG9WTXCUIYUCGCMWNA99NYHABE9B'), 1410751498386),
            (TransactionHash(b'ZVEYLIAXGAJAZP9NDHNWSIIJBZNETCSPJRSBGXVXSIAFUAZHKUDGIACFQJFRGZKUPZCYSMDJGWOCHWYAC'), 10000000),
            (TransactionHash(b'JCOVBKZLFCTBDFDLNRIIZTMBBCQVSCGZYGJXJIZGJTUVBPYYILERZMBWDHDGBTGLUZJB9BEXSZOQIZHMD'), -1410776498386)
        ]

        self.assertListEqual(value, expect)

        # Bad
        self.assertIsNone(self.provider.get(iota.TryteString('9' * (iota.Hash.LEN - 1) + 'A'), 'state_diff'))
        self.assertIsNone(self.provider.get(iota.TransactionHash('FOOBAR'), 'state_diff'))
        with self.assertRaises(ValueError):
            self.assertIsNone(self.provider.get(iota.TryteString('FOOBAR'), 'state_diff'))
        with self.assertRaises(TypeError):
            self.provider.get('', 'state_diff')


    def test_bad_column_value_should_raise_key_error(self):
        with self.assertRaises(KeyError):
            self.provider.get(259773, 'milestones')
        with self.assertRaises(KeyError):
            self.provider.get(iota.Hash('EXAMPLE'), 'tags')
        with self.assertRaises(KeyError):
            self.provider.get(None, '')

    def test_bad_column_type_should_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.provider.get(None, b'')
        with self.assertRaises(TypeError):
            self.provider.get(None, None)
        with self.assertRaises(TypeError):
            self.provider.get(None, 100)

    def test_next_transaction(self):
        key = iota.TransactionHash('PZYRMRVTSPQXNEQIQEBAGINMDAKOHPOLNH9LR9DTFWMWFQICXL9BJCWBUPMKZERKYKBDRIBYEJYH99999')
        value = self.provider.next(key, 'transaction')

        self.assertEqual(value[0], iota.TransactionHash('PZYUVYZADTFXQSJCMNVOUKDKOMOBEPLQSKJGNZGCKSXOSXEJKUBTUQZGOFMVDTLXBDYABFIVGZ9JZ9999'))

    def test_next_milestone(self):
        key = 250000
        value = self.provider.next(key, 'milestone')

        self.assertEqual(value[0], key + 1)

    def test_first_milestone(self):
        key, value = self.provider.first('milestone')
        self.assertEqual(key, 243001)
        self.assertEqual(value, (243001, iota.TransactionHash(b'9PPVIKDMKUDXTYJFF9YNWUPPMOYZTYKRBFGLGDCNNNIMWAMGVJGEHOCOUDYRVYPPSDKDKDQXUBMYA9999')))

    def test_latest_milestone(self):
        key, value = self.provider.latest('milestone')
        self.assertIsInstance(key, int)
        self.assertIsInstance(value, tuple)

    def test_first_transaction(self):
        key, value = self.provider.first('transaction')

        self.assertIsInstance(key, iota.TransactionHash)
        self.assertIsInstance(value, iota.Transaction)

    def test_latest_transaction(self):
        key, value = self.provider.latest('transaction')

        self.assertIsInstance(key, iota.TransactionHash)
        self.assertIsInstance(value, iota.Transaction)

    @unittest.expectedFailure
    def test_may_exist(self):
        # XXX: This function is not work now
        key = iota.TransactionHash('PZYRMRVTSPQXNEQIQEBAGINMDAKOHPOLNH9LR9DTFWMWFQICXL9BJCWBUPMKZERKYKBDRIBYEJYH99999')
        self.assertTrue(self.provider.may_exist(key, 'transaction'))
        self.assertFalse(self.provider.may_exist(iota.Hash('FOOBAR'), 'transaction'))


if __name__ == '__main__':
    unittest.main()
