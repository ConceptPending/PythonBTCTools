import random, os, binascii

def rand_string(len=32):
    t = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    string = ''
    for x in range(0,len):
        string = string + random.choice(t)
    return string

def rand_hex(len=32):
    return binascii.b2a_hex(os.urandom(len))
