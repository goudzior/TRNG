
import os
import hmac_drbg as prng

def trim_bits(value, num_bits):
    # Masks the value to retain only the most significant 'num_bits' bits.
    return value & ((1 << num_bits) - 1)

def extract_entropy(folder):
    # Collects entropy from binary files within a folder.
    entropy_bits = b''
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                entropy_bits += file.read().strip()
    return entropy_bits

def main():
    rtt_folder = 'RTTS'
    random_bytes = 1
    bit_length = 8

    entropy_bits = extract_entropy(rtt_folder)
    #combined_entropy_bits = combine_entropy_bits([entropy_bits])
    seed = prng.secrets.randbits(256).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)
    prng_value = drbg.generate(random_bytes)

    prng_value = trim_bits(int.from_bytes(prng_value, 'big'), bit_length)
    print (f'entropy b: {entropy_bits}')
    entropy_bits = int.from_bytes(entropy_bits, 'big')
    print (f'entropy int: {entropy_bits} entropy bin: {bin(entropy_bits)}')

    entropy_bits = trim_bits(entropy_bits, bit_length)
    print (f'entropy trimmed: {entropy_bits}')

    random_numbers = []

if __name__ == "__main__":
    main()