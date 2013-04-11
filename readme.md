Python Bitcoin Tools
========================

This is a utility that allows various Bitcoin operations in Python with the only dependency being the ECDSA library.

Assuming you have the ECDSA library installed (`pip install ecdsa`), you can generate a Key object using the following code:

    >>> from btctools import Key
    >>> newkey = Key()

Now you can access the private key, address, and WIF format private key from the Key class.

    >>> newkey.pk
    'b7da99b7348a1eb845debcac6d7f7688a709e3122a2fa4aa4bdfc77f82502bea'
    >>> newkey.address
    '1NnBx3eXsEdoREaJY3cHw9YEBHekaz5yJm'
    >>> newkey.wif
    '5KDFtA6fSXSUaLPT6YJuLvpRvbmgpzwcoBLWq1pgDzsqUniuM5o'

If you'd rather use a Generator to output an arbitrary number of private keys and addresses, you can do that as well.

    >>> from btctools import key_gen
    >>> kg = key_gen()
    >>> kg.next()
    ('3f27cc98fe145eafa00178f6d490c05d9d0ad53da144c2277670a03a3c61f96a', '1P1ysyzHyHENDuoQKGQVZttPkTw5K4Y1QF')
    >>> kg.next()
    ('b0c731221ceb3b5208f75e933d824c9ec0d2a9a2f711cb51020db75646f7c188', '1LrX1wkBj15BtKJx8PptLR1AWGdvkPg7At')
