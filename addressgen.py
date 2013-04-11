import hashlib, binascii, rand_string, ecdsa

t='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

secp256k1curve=ecdsa.ellipticcurve.CurveFp(115792089237316195423570985008687907853269984665640564039457584007908834671663,0,7)
secp256k1point=ecdsa.ellipticcurve.Point(secp256k1curve,0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)
secp256k1=ecdsa.curves.Curve('secp256k1',secp256k1curve,secp256k1point,(1,3,132,0,10))

"""The initial version of the 'numtowif', 'wiftonum', gen_addy, and 'validwif' functions
are contributed by JeromeS at BitcoinTalk.org
https://bitcointalk.org/index.php?topic=84238.0"""
def numtowif(numpriv):
    step1 = '80'+hex(numpriv)[2:].strip('L').zfill(64)
    step2 = hashlib.sha256(binascii.unhexlify(step1)).hexdigest()
    step3 = hashlib.sha256(binascii.unhexlify(step2)).hexdigest()
    step4 = int(step1 + step3[:8] , 16)
    return ''.join([t[step4/(58**l)%58] for l in range(100)])[::-1].lstrip('1')

def wiftonum(wifpriv):
    return sum([t.index(wifpriv[::-1][l])*(58**l) for l in range(len(wifpriv))])/(2**32)%(2**256)

def validwif(wifpriv):
    return numtowif(wiftonum(wifpriv))==wifpriv

def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return to_bytes(n, length)

def encode_base58(raw):
    if type(raw) == 'str':
        raw = int(raw, 16)
    return ''.join([t[raw/(58**l)%58] for l in range(100)])[::-1].lstrip('1')

# This was nasty to figure out from the code posted on RosettaCode as I believe it only works on Python 3 as written.
def to_bytes(n, length):
    bytelist = ''
    for i in reversed(range(length)):
        bytelist = bytelist + chr(int(bytes(n >> i*8 & 0xff)))
    return bytelist

# From RosettaCode http://rosettacode.org/wiki/Bitcoin/address_validation#Python
def check_bc(bc):
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == hashlib.sha256(hashlib.sha256(bcbytes[:-4]).digest()).digest()[:4]

def new_pk():
    priv_key = rand_string.rand_hex(32)
    while ( 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 < int(priv_key,16) < 0x1 ):
        priv_key = rand_string.rand_hex(32)
    return priv_key

def new_addy(pk):
    # Additional check for PK string to convert to int
    if type(pk) == str:
        pk = int(pk, 16)
    pko=ecdsa.SigningKey.from_secret_exponent(pk,secp256k1)
    pubkey=binascii.hexlify(pko.get_verifying_key().to_string())
    pubkey2=hashlib.sha256(binascii.unhexlify('04'+pubkey)).hexdigest()
    pubkey3=hashlib.new('ripemd160',binascii.unhexlify(pubkey2)).hexdigest()
    pubkey4=hashlib.sha256(binascii.unhexlify('00'+pubkey3)).hexdigest()
    pubkey5=hashlib.sha256(binascii.unhexlify(pubkey4)).hexdigest()
    pubkey6=pubkey3+pubkey5[:8]
    pubnum=int(pubkey6,16)
    pubnumlist=[]
    while pubnum!=0: pubnumlist.append(pubnum%58); pubnum/=58
    address=''
    for l in ['123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'[x] for x in pubnumlist]:
        address=l+address
    return '1'+address

class Key:
    """This will hold the following information:
        Private Key in both String and Int form
        WIF String
    """
    def __init__(self, pk_init=new_pk()):
        self.pk = pk_init
        self.wif = numtowif(int(self.pk,16))
        self.address = new_addy(self.pk)
