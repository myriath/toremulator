import sys
import encryptor


keys = []
ivs = []


def test_encryption():
    print(keys)
    print(ivs)

    msg = b"HELLO WORLD!"
    print(f"MESSAGE: {msg}")
    encrypted = encryptor.totalencrypt(keys, msg, ivs)
    encrypted1 = encryptor.encrypt(keys[0], msg, ivs[0])
    encrypted2 = encryptor.encrypt(keys[1], encrypted1, ivs[1])
    encrypted3 = encryptor.encrypt(keys[2], encrypted2, ivs[2])
    print(encrypted)
    print(encrypted3)
    print(encrypted3 == encrypted)
    decrypted = encryptor.totaldecrypt(keys, encrypted, ivs)
    decrypted3 = encryptor.decrypt(keys[2], encrypted3, ivs[2])
    decrypted2 = encryptor.decrypt(keys[1], decrypted3, ivs[1])
    decrypted1 = encryptor.decrypt(keys[0], decrypted2, ivs[0])
    print(decrypted)
    print(decrypted1)
    print(msg)
    print(decrypted1 == decrypted)


def main():



if __name__ == "__main__":
    if "genkeys" in sys.argv:
        encryptor.genkeys(keys, ivs)
    else:
        encryptor.readkeys(keys, ivs)

    main()
