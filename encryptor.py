from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
from base64 import b64decode, b64encode


KEY_PATH = 'keys/key'
IV_PATH = 'keys/iv'


def genkeys(keys, ivs):
    for i in range(3):
        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        with open(f'{KEY_PATH}{i+1}', 'wb') as f:
            f.write(key)
        with open(f'{IV_PATH}{i+1}', 'wb') as f:
            f.write(iv)
        keys.append(key)
        ivs.append(iv)


def readkeys(keys, ivs):
    try:
        for i in range(3):
            with open(f'{KEY_PATH}{i+1}', 'rb') as f:
                keys.append(f.read())
            with open(f'{IV_PATH}{i+1}', 'rb') as f:
                ivs.append(f.read())
    except IOError:
        keys.clear()
        ivs.clear()
        genkeys(keys, ivs)


def encrypt(key, msg, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)

    msg = Padding.pad(msg, AES.block_size)
    ciphertext = cipher.encrypt(msg)
    return b64encode(ciphertext)


def decrypt(key, b64msg, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = b64decode(b64msg)
    plaintext = cipher.decrypt(ciphertext)
    return Padding.unpad(plaintext, AES.block_size)


def totalencrypt(keys, msg, ivs):
    encrypted = msg
    for i in range(len(keys)):
        encrypted = encrypt(keys[i], encrypted, ivs[i])
    return encrypted


def totaldecrypt(keys, ciphertext, ivs):
    decrypted = ciphertext
    for i in reversed(range(len(keys))):
        decrypted = decrypt(keys[i], decrypted, ivs[i])
    return decrypted
