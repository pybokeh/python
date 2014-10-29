# This code taken from youtube example: https://www.youtube.com/watch?v=8PzDfykGg_g&feature=youtube_gdata_player
# but modified to work with Python 3 due to byte string to string conversion using decode('utf-8') method
# Windows binary installer can be obtained here: http://www.voidspace.org.uk/python/modules.shtml#pycrypto

from Crypto.Cipher import AES  # Dependency: install pycrypto - available at pypi: pip install pycrypto
import base64
import os
import codecs # This is needed to convert a string with single backslashes to byte string

def encrypt(privateInfo):
    """ Method to encrypt your message using AES encryption """
    
    BLOCK_SIZE = 16
    PADDING = '{'

    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    secret = os.urandom(BLOCK_SIZE)  # Comment this line and uncomment line below to use hard-coded key
    #secret = b"7\xcd\xf0\xbe\xd4\x95pa'+c\xe0\xeeX\x9a\x07"
    print('Encryption key:', secret)

    cipher = AES.new(secret)

    encoded = EncodeAES(cipher, privateInfo)
    print('Encrypted string:', encoded.decode('utf-8'))


def encrypt_with_key(key, privateInfo):
    """ Method to encrypt your message using AES encryption """
    
    BLOCK_SIZE = 16
    PADDING = '{'

    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    cipher = AES.new(codecs.escape_decode(key)[0])  # Need to use codecs to prevent key from being parsed with double slashes

    encoded = EncodeAES(cipher, privateInfo)
    return encoded.decode('utf-8')



def decrypt_key_hardcoded(encryptedString):
    """ Method to decrypt message using a hard-coded decryption key """
    
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).decode('utf-8').rstrip(PADDING)
    #DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    key = b'\xf9J\xa4\xd1\t\x17\xb8\xabt\xfe\x06\x96\xe3\xe8(.'
    try:
        cipher = AES.new(key)
        decoded = DecodeAES(cipher, encryptedString)
        return decoded
    except:
        return "Error in decoding the secret message"

def decrypt_with_key(key, encryptedString):
    """ Method to decrypt message using a decryption key passed in as a parameter """
    
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).decode('utf-8').rstrip(PADDING)
    try:
        cipher = AES.new(key)
        decoded = DecodeAES(cipher, encryptedString)
        return decoded
    except:
        return "Error in decoding the secret message"

#key = codecs.escape_decode(open('file_path','r').read().strip())[0]
#pw  = open('file_path','r').read().strip()
