from Crypto.Cipher import AES  # Dependency: install pycrypto - available at pypi: pip install pycrypto
import base64
import os

def encryption(privateInfo):
    BLOCK_SIZE = 16
    PADDING = '{'

    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    #secret = os.urandom(BLOCK_SIZE)
    secret = b'\xf9J\xa4\xd1\t\x17\xb8\xabt\xfe\x06\x96\xe3\xe8(.'
    print('Encryption key:', secret)
    print('Type of key:', type(secret))

    cipher = AES.new(secret)

    encoded = EncodeAES(cipher, privateInfo)
    print('Encrypted string:', encoded)
    print('Type of encrypted string:', type(encoded))


def decryption(encryptedString):
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).decode('utf-8').rstrip(PADDING)
    #DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    key = b'\xf9J\xa4\xd1\t\x17\xb8\xabt\xfe\x06\x96\xe3\xe8(.'
    cipher = AES.new(key)
    decoded = DecodeAES(cipher, encryptedString)
    print('Decoded:', decoded)

#encryption("111-111-1111")
decryption(b'wkFk96FfUxhYmkfr/zbjAw==')
