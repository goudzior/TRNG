import hashlib
import hmac
import secrets

class DRBG(object):
    def __init__(self, seed):
        self.key = b'\x00' * 64
        self.val = b'\x01' * 64
        self.reseed(seed)

    def hmac(self, key, val):
        return hmac.new(key, val, hashlib.sha512).digest()

    def reseed(self, data=b''):
        self.key = self.hmac(self.key, self.val + b'\x00' + data)
        self.val = self.hmac(self.key, self.val)

        if data:
            self.key = self.hmac(self.key, self.val + b'\x01' + data)
            self.val = self.hmac(self.key, self.val)

    def generate(self, n):
        xs = b''
        while len(xs) < n:
            self.val = self.hmac(self.key, self.val)
            xs += self.val

        self.reseed()

        return xs[:n]

# Generating random seed using secrets library
seed = (secrets.randbits(256)).to_bytes(32)
drbg = DRBG(seed)

# Generate 5 random numbers (test purposes)
for i in range(5):
    drbg.reseed
    generated_number = int.from_bytes(drbg.generate(1))
    print(generated_number)

