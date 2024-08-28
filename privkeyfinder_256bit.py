#PRIVATE KEY FINDER (i guess)
# PUZZLE 66 BTC address => 13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so
# BALANCE => 6.60061163
# public key => 20d45a6a762535700ce9e0b216e31994335db8a5
# bitcoin address => 13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so

# pubkey_to_address -> takes P2PKH(compressed) hash160
# privkey_to_address(compressed) -> takes WIF(compressed)
# privkey_to_address(uncompressed) -> takes WIF(uncompressed)


from hashlib import sha256
import base58
import cryptos
# import secrets
import random
import os
from time import sleep
import threading
import sys
# from cryptos import *

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    
def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def privToWIF(private_key):
    # Step 1: Add version byte (0x80 for mainnet)
    versioned_key = '80' + private_key
    
    # Step 3: Double SHA-256 hash
    first_sha = sha256(bytes.fromhex(versioned_key)).hexdigest()
    second_sha = sha256(bytes.fromhex(first_sha)).hexdigest()
    
    # Step 4: Add first 4 bytes of the second SHA-256 hash as checksum
    checksum = second_sha[:8]
    final_key = versioned_key + checksum
    
    # Step 5: Encode in Base58Check
    compressed_private_key = base58.b58encode(bytes.fromhex(final_key)).decode('utf-8')
    
    return compressed_private_key
                      
def compress_private_key(private_key_hex):
    # Step 1: Add version byte (0x80 for mainnet)
    versioned_key = '80' + private_key_hex
    
    # Step 2: Add compression byte (0x01)
    compressed_key = versioned_key + '01'
    
    # Step 3: Double SHA-256 hash
    try:
        sha = sha256(bytes.fromhex(sha256(bytes.fromhex(compressed_key)).hexdigest())).hexdigest()
    except Exception as e:
        print(private_key_hex)
        with open(os.path.join(os.path.expanduser("~"), "Desktop\\privkey.txt"),"a") as f:
            f.write("\n" + f"Bozuk hex: {private_key_hex} \n Compressli Bozuk Hex: {compress_private_key(private_key_hex)}\n")
        return compress_private_key(private_key_hex)
    # Step 4: Add first 4 bytes of the second SHA-256 hash as checksum
    checksum = sha[:8]
    final_key = compressed_key + checksum
    
    # Step 5: Encode in Base58Check
    compressed_private_key = base58.b58encode(bytes.fromhex(final_key)).decode('utf-8')
    
    return compressed_private_key

def randomGenPrivKey(start, end, addr): #inclusive
    # a = int_to_bytes(secrets.randbelow(end - start + 1) + start)
    global a
    while True:
        # a = hex(secrets.randbelow(end - start + 1) + start)[2:]
        a = hex(random.SystemRandom().randint(start,end))[2:]
        # print(a)
        # sleep(0.3)
        while len(a) < 64:
                if len(a) < 64:
                    a = '0' + a
        if(addr == cryptos.privkey_to_address(compress_private_key(a))):
            wif = privToWIF(a)
            with open(os.path.join(os.path.expanduser("~"), "Desktop\\privkey.txt"),"a") as f:
                f.write("\n" + f"Private Key: {a}" + "\n" + f"WIF Private Key: {wif}"+"\n" + f"WIF COMPRESSED Private Key:{compress_private_key(a)}" + "\n")
            print("\n" + f"Private Key: {a}" + "\n" + f"WIF Private Key: {wif}"+"\n" + f"WIF COMPRESSED Private Key:{compress_private_key(a)}" + "\n")
            return a
        sleep(0.001)        

def genkeyrand(addr,b):
    # a = int_to_bytes(secrets.randbelow(end - start + 1) + start)
    global a
    while True:
        # a = hex(secrets.randbelow(end - start + 1) + start)[2:]
        a = hex(random.SystemRandom().randint(4,10))[2:]
        # print(a)
        # sleep(0.3)
        while len(a) < 64:
                if len(a) < 64:
                    a = '0' + a
        if(addr == cryptos.privkey_to_address(compress_private_key(a))):
            wif = privToWIF(a)
            with open(os.path.join(os.path.expanduser("~"), "Desktop\\privkey.txt"),"a") as f:
                f.write("\n" + f"Private Key: {a}" + "\n" + f"WIF Private Key: {wif}"+"\n" + f"WIF COMPRESSED Private Key:{compress_private_key(a)}" + "\n")
            print("\n" + f"Private Key: {a}" + "\n" + f"WIF Private Key: {wif}"+"\n" + f"WIF COMPRESSED Private Key:{compress_private_key(a)}" + "\n")
            return a
        sleep(0.001) 

if __name__ == "__main__":
    print("\n\nCrack operation has start! ...\n")
    # randomGenPrivKey(2**65,2**66-1,"13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so")
    # genkeyrand("13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so")
    threads = []
    for i in range(4):  # Number of threads
        # t = threading.Thread(target=genkeyrand, args=("13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so",2))
        t = threading.Thread(target=genkeyrand, args=(sys.argv[1],2))


        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()
