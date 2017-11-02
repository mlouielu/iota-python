IOTA-Python - A Pure-Python implementation of IOTA node
=======================================================

The target of this project is to create a pure Python implementation of IOTA node.


## Current Develop Status

* rocksdb readable


## Getting Started

### Dependencies

* rocksdb

You can see the rocksdb install guide from
[facebook/rocksdb - INSTALL.md](https://github.com/facebook/rocksdb/blob/master/INSTALL.md).

For Arch Linux user, simply typing:

```
$ yaourt -S rocksdb
```

### Requirements

* [python-rocksdb-iota](https://github.com/mlouielu/python-rocksdb)
* [pyota](https://github.com/iotaledger/iota.lib.py)

### Installation of IOTA-Python

#### $ pipenv install iotapy

To install IOTA-Python, simply run this simple command in your terminal of choice:

```
$ pipenv install iotapy
```

#### Get the Source Code

IOTA-Python is actively developed on GitHub, where the code is
[always available](https://github.com/mlouielu/iota-python).

You can clone the source code from repository:

```
$ git clone https://github.com/mlouielu/iota-python
```

Once you have a copy of source code, you can install the package easily:

```
$ cd iota-python
$ pip install -r requirements.txt
$ python setup.py install
```

## Tutorials - About RocksDBProvider

This is a tutorial of IOTA-Python to read the database from java IRI, and this
is what IOTA-Python can do now.

### Open IRI rocksdb

Remember, make sure `db_path` and `db_log_path` is point to *your* database path.
At this point, IOTA-Python didn't support writing data back to the database (also,
it have a lock on it, if you want to write it), so `read_only` should also be `True`.

```python
>>> import iota
>>> import iotapy
>>> r = iotapy.storage.providers.rocksdb.RocksDBProvider(
        db_path='/var/db/iota/mainnetdb',
        db_log_path='/var/db/iota/mainnetdb.log',
        read_only=True
    )
>>> r.init()   # Absolute remember to init database
>>>
```

### Access IRI rocksdb

Now you open the database, you can get the data inside it! IRI using rocksdb
column family to separate the data stored. For column family list, please visit
this [blog post](https://blog.louie.lu/2017/10/31/iota-iri-rocksdb-data-storage-structure/)

Now, we can try to open a transaction, here we got an example transaction hash:
`GTXDTJVUTVSNHYFPJUOWFKTGQTCMNKZPJDJXSWVQWTXYRDZAVZTX9KFBRIMRQEQLMCMVAUKMZWMHA9999`.

You can check this tx information at this
[page](https://thetangle.org/transaction/GTXDTJVUTVSNHYFPJUOWFKTGQTCMNKZPJDJXSWVQWTXYRDZAVZTX9KFBRIMRQEQLMCMVAUKMZWMHA9999)

```python
>>> txh = iota.TransactionHash('GTXDTJVUTVSNHYFPJUOWFKTGQTCMNKZPJDJXSWVQWTXYRDZAVZTX9KFBRIMRQEQLMCMVAUKMZWMHA9999')
>>> column_family = 'transaction'
>>> tx = r.get(txh, column_family)
>>> tx.tag
Tag(b'EXAMPLEPYTHONLIB99999999999')
>>> tx.bundle_hash
BundleHash(b'CRNTWYOGTYKPAHYHNESJOKLRFYQQGCXXUZIZQFTCCLSTZODTRBPZWTX9TVHNDNNIWTULV9GFLAPPSTCC9')
>>> tx.signature_message_fragment
Fragment(b'RBTC9D9DCDFAEACCWCXCGDEAXCGDEAPCEAHDTCGDHDEAUCFDCDADEAZBMDHDWCCDBD999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999')
>>> tx.signature_message_fragment.as_string()
'Hello! This is a test from Python'
>>> tx.as_json_compatible()
{
    'hash_': ...,
    'signature_message_fragment': ...,
    'address': Address(b'9TPHVCFLAZTZSDUWFBLCJOZICJKKPVDMAASWJZNFFBKRDDTEOUJHR9JVGTJNI9IYNVISZVXARWJFKUZWC'),
    'value': 0,
    'legacy_tag': ...,
    'timestamp': 1508993435,
    'current_index': 0,
    'last_index': 0,
    'bundle_hash': ...,
    'trunk_transaction_hash': ...,
    'branch_transaction_hash': ...,
    'tag': Tag(b'EXAMPLEPYTHONLIB99999999999'),
    'attachment_timestamp': 1508993445508,
    'attachment_timestamp_lower_bound': 0,
    'attachment_timestamp_upper_bound': 12,
    'nonce': Nonce(b'HYNAKUFLKW9UZXXIDJFGUMUDDVX')
}
>>>
```

If you are using method such as `RocksDBProvider.get`, `RocksDBProvider.latest`,
please use the following column family name:

```
address
approvee
bundle
milestone
state_diff
tag
transaction
transaction_metadata
```


The full list of column family name can be found at `RocksDBProvider.column_family_names`,
but this list is used for low level database access, it only used at `RocksDBProvider.db`.

```
b'default'
b'transaction'
b'transaction-metadata'
b'milestone'
b'stateDiff'
b'address'
b'approvee'
b'bundle'
b'tag'
```

Example of `RocksDBProvider` methods:

```python
# Get address' transaction record
>>> adr = iota.Address('9TPHVCFLAZTZSDUWFBLCJOZICJKKPVDMAASWJZNFFBKRDDTEOUJHR9JVGTJNI9IYNVISZVXARWJFKUZWC')
>>> r.get(adr,'address')
<generator object get at 0x7eff2b341518>

# Get next address (in database)
>>> r.next(adr, 'address')
(Address(b'9BPQJPGAMDVKAQ9FDPQSVINPMHSIUUXKYMIZQGPBDGGEUZGLEVFIWUYO9MEIPOYUBYVQGJCFYRWTQENCZ'), <generator object get at 0x7eff2b3415c8>)

# Get first milestone
>>> r.first('milestone')
(243001, (243001, TransactionHash(b'9PPVIKDMKUDXTYJFF9YNWUPPMOYZTYKRBFGLGDCNNNIMWAMGVJGEHOCOUDYRVYPPSDKDKDQXUBMYA9999')))

# Get latest milestone
>>> r.latest('milestone')
(265486, (265486, TransactionHash(b'TFWZVEQZGQGBUBKMFA9YKBVDGBWWMXWCGGYYAGPZKGXWKJQRUNSMXJBSVVGYRJKCS9GNWULQSMAGZ9999')))

# Get next milestone
>>> key, value = r.first('milestone')
>>> r.next(key, 'milestone')
(243002, (243002, TransactionHash(b'XHIOO9EJ9H9ULPJM9MIJSTPHNPIUAAJ9NLYHZLHDBCSECCJVRGDWHTRUEUIQXWVLBYOCBNHFWWWPA9999')))
```

Low level db access (something you don't need to touch at this moment):

```python
>>> column_handler = r.db.column_family_handles[b'transaction-metadata']
>>> txh = iota.TransactionHash('GTXDTJVUTVSNHYFPJUOWFKTGQTCMNKZPJDJXSWVQWTXYRDZAVZTX9KFBRIMRQEQLMCMVAUKMZWMHA9999')
>>> key = iotapy.storage.converter.from_trits_to_binary(txh.as_trits())
>>> value = r.db.get(key, column_handler)
b"6\x8d\xd6\xb2v\xf7\xde9\xcb\xab\x07\x1f\xb9\xfc\x1e@s\xcfpU\xb8\x17\xad2<!!:\x0e\xc6\xef\xe6Z\xc5=\x8e\tl\x8a\xfb\x98\xd3\x18\x94Y<\x9e\xdc\x03\x03\x87\xda\xad\xc3\xec\xd5\xb1\xf1\x9c_W*%3\xe32\x1d\xac\x9dQ\xe4\xc0\x19T\x98\xf5`\xeb\x0f\xda\xa3\xe36\x9f\x8e\x98\xd8\xdfJt\xfe\xb6v\x9d\x10\xea\x1c\x00\xdc\xf6>3Wf\xd52\xb5\xe0\xc4\xb7\xd5\xb6\xcb\xb7\xc1\xdb$\xad%\xd4\xa2\xf3\xefI'\xd5\xa7Y\xe2\xa5]G\x9e\xb82\xd7\x1f&\x9cR4\xa7\x13\xff\x00\x00\x00!\x0c;\xa2\x1b\xc6-\xa0\xd5\xbe\xaa*\xb1\x95\xbcUI\xb5l\x89\xa1\xe3\xacn\x90@\x10\xdf\xf9Un\xb7\xb1\x93\x9b\xc7\x017:o\xba\xd8\xfdq\xff\xe2\x00\x00\x00\xb4T\xa1\xa01\xc0\xb7\xd8U\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Y\xf1i\x9b\xb4T\xa1\xa01\xc0\xb7\xd8U\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01_W\x04\xae\x84\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00Y\xf1i\xa5\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x03\xd6\xe0local"
>>>
```

### EXPLOSION! An example of exploring the IRI database!

![](https://pm1.narvii.com/6258/7f113d43b699f954c3d65df5aa5f397936363099_hq.jpg)

*EXPLOSION!*

Glade you are here, now you gain the full access power of the IRI database.

We all know that IOTA is a DAG, that is, theoretically speaking, we can start
from a transaction, and go to its parent, and its parent, and its parent...and
we will finally get to the genesis address / node / block whatever.

Here is a small script that I trying to find this answer:

```python
import time
import iota
import iotapy


# Initialize the database
r = iotapy.storage.providers.rocksdb.RocksDBProvider(
        db_path='/var/db/iota/mainnetdb',
        db_log_path='/var/db/iota/mainnetdb.log',
        read_only=True)
r.init()


# We will start from this transaction
txh = iota.TransactionHash('UNUK99RCIWLUQ9WMUT9MPQSZCHTUMGN9IWOCOXWMNPICCCQKLLNIIE9UIFGKZLHRI9QAOEQXQJLL99999')
tx = r.get(txh, 'transaction')

# Stop at here
EMPTY = iota.TransactionHash('9' * 81)

# Go to find the genesis!
i = 0
while True:
    i += 1
    if i % 100 == 0:
        print(txh, time.ctime(tx.timestamp))

    # Branch is outside the bundle and trunk is in the bundle
    # So we choose branch at here
    if tx.branch_transaction_hash != EMPTY:
        txh = tx.branch_transaction_hash
        tx = r.get(tx.branch_transaction_hash, 'transaction')
    else:
        # This is the end of the journey
        print("\nProbably the genesis?")
        print(txh)
        break

```

It will run like:

```
NQRZKAE9CDFGJUPOMTHCVPOQE9LENTSHNJYDXCWZJ9IRXKLWTGRIHYZCZWSEIOKQFVBBEBNTXHNBA9999 Thu Oct 26 11:23:31 2017
KMRPH9BVZVFRCEGDEROQBMZTNOQECYRKIJJ9MWGNOUMWVPLFIJ9PRANLDXSTZCVJGHTXTYCWYGJFZ9999 Thu Oct 26 08:40:52 2017
JQLXELCKS9QSNWZNHJJICAQMGZRTGFPGNRRNJWTBEPZWKEHLJINXVLPOMMQCMQSOEUZGRHSKBNWEA9999 Thu Oct 26 06:40:31 2017
IOKLUAGDGKSU9RGHZXCQJIBRTFPCNVCIVG9TQNIGE9DVIYIUDCEVTMPYBZQXHNYLNSNFTXDWNH9BA9999 Thu Oct 26 05:41:28 2017
AUEDLXAJZPW9URCQZABSRNJGYOOSDG9OFHUMXINMVULHOIVWOBDLSSS9DPNTSXHTDKG9MGKMUESD99999 Thu Oct 26 04:38:37 2017
DZRYEISPEUXXVQMGBSPVMOFFTWPDYQ9EWVYZUQTNX9NPSEWRGNMSZMY9BOTABSLPCTKMIGWAAIPJA9999 Thu Oct 26 03:45:03 2017
UPAIBMKZEOTUEHHLEYZEEKZFLDGWHWJ9UZLGLRV9NGZPWSGWY9DPITWSDZPQQZDBOYFJDLJYTDKXZ9999 Thu Oct 26 02:51:53 2017
MZPRET9XVFBK9LQZLFNN9UGQLLBYAVGAKJGODQIKVZWHPDLZQLOTFMMGEAGSGWGPEYBLJLLJJXOEZ9999 Thu Oct 26 02:08:16 2017
XPMVSHVFNKYSTKPSHLPHDQCKEGWTERKEHTDRUKIQRE9KDDQVAQHUOQHYOPTRZGIIQHLYGYCPTLAEA9999 Thu Oct 26 01:17:58 2017
MHDQIXDMBOFHCOMLGNHPSJGNIXIDAQQNW9CJKSXPYIOIITQES99KNYTPNPOQBTVZQXYOKBVEIZB999999 Thu Oct 26 00:37:14 2017
...
GXWKBVNFPFX99PGDCH9EQZMLHITMBFAPDQRNNGNGOOXYXEEYYDDDFWJRDQINOEJFSITMEUY9VMVO99999 Tue Oct 24 06:37:13 2017
UAPTGGCKCGCPWGVQEKBCPKNQUWOPVRBAFAQYHSDU9AJMVINJFVZSM9URBYUAIHCPKOJRBWSOOSHLZ9999 Tue Oct 24 06:16:17 2017
FPPJWECLHTF9HGGEMNH9FUIAVYJWDOIOXYFRRJ9S9HENTSESTGJYLYOSNNJGKDOUOGXOWFURNDNEZ9999 Tue Oct 24 05:56:10 2017
HSDV9SKUYCBWNXFIHKLNAXEVPDTGLSPMTMTXCYISS9M9SPL9DERO9GCQLNWY9KBIHOLPYBCTCYECA9999 Tue Oct 24 05:35:44 2017
LQPVJDHGQPILXVUPCCZGJMCAQHROJLHQKBILEUDBKQAEHMHEOEK9GMRDWEKVRXRB99TOYQQLTZDGZ9999 Tue Oct 24 05:14:13 2017
FOCMONRMEOBQEBDOJOQPOOPLRIYCI9PMSJXXNEWAZPBRCDGZTZB9KI9SSMKKFBGBDONMILXWOBEFA9999 Tue Oct 24 04:53:03 2017
BEFSRMKVEWXXHERTONXCQLOAVQYVRPFFZCQIDGUOLLZCFLTRPRHEVYNAPQFKGJOCDAJYNVUJDQIRZ9999 Tue Oct 24 04:32:48 2017
QVHPAOWGDFTTLYQERDRNBBNCJJCWTJSDBIKBLDYZOLJ9PWFWFWUXP9DGPKTLRZDFZNLFRYXSZF9O99999 Tue Oct 24 04:12:07 2017

Probably the genesis?
9PPVIKDMKUDXTYJFF9YNWUPPMOYZTYKRBFGLGDCNNNIMWAMGVJGEHOCOUDYRVYPPSDKDKDQXUBMYA9999
```

Check this transaction on [thetangle](https://thetangle.org/transaction/9PPVIKDMKUDXTYJFF9YNWUPPMOYZTYKRBFGLGDCNNNIMWAMGVJGEHOCOUDYRVYPPSDKDKDQXUBMYA9999)

## Documentation

~~Source code is your best friend~~

Documentation is still under construct.
