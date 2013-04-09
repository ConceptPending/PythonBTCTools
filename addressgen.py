import hashlib, binascii, rand_string

t='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

"""The initial version of the 'numtowif', 'wiftonum', and 'validwif' functions
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

def new_priv_key():
    priv_key = rand_string.rand_hex(32)
    while ( 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 < int(priv_key,16) < 0x1 ):
        priv_key = rand_string.rand_hex(32)
    return priv_key

class Key:
    """This will hold the following information:
        Private Key in both String and Int form
        WIF String
    """
    def __init__(self, priv_key_init=new_priv_key()):
        self.priv_key = priv_key_init
        self.wif = numtowif(int(self.priv_key,16))
