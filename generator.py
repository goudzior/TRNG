import hmac_drbg as prng
import round_trip_time as rtt
import numpy as np
import csv
    
def check_bitlength(file):
    with open(file, 'rb') as file:
        file.seek(0, 2)  # Move the file pointer to the end of the file
        bit_length = file.tell() * 8  # Get the byte length and convert it to bits
    return bit_length

def read_random_url(file):
    with open(file, 'r') as file:
        # Read all lines from the text file
        lines = file.readlines()
        # Choose a random line (URL) from the list
        random_url = prng.secrets.choice(lines).strip()  # Strip to remove newline characters
    return random_url
    
def extract_entropy(filename):
    entropy_bits = ''
    with open(filename, 'r') as file:
        for line in file:
            # Convert each round trip time to binary representation and append to the bitstring
            round_trip_time = int(line.strip())
            binary_rep = bin(round_trip_time)[2:]  # Convert to binary, strip '0b' prefix
            entropy_bits += binary_rep
    return entropy_bits

def main():
    bitlength = 1
    num_measurements = 1
    num_urls = 1
    rtt_data = 'RTT_ns.txt'
    url_data = 'top_websites.txt'

    with open(rtt_data, 'w') as file:  # Open the file in write mode to clear its contents
        pass

    with open(rtt_data, 'a') as file:
        for i in range(num_urls):
            url = 'https://' + read_random_url(url_data)
            #print(f"Measuring for: {url}")
            for _ in range(num_measurements):
                round_trip_time = rtt.measure_round_trip_time(url)
                #print(f"Round trip time: {round_trip_time} nanoseconds")
                file.write(str(round_trip_time) + '\n')
    #print(f"Round trip times saved to {rtt_data}")

    # Display the bitlength of rtt file
    #print(f"Bit length of rtt_ns.txt: {check_bitlength(rtt_data)} bits")
    # TODO => add health tests

    bitstring = extract_entropy('RTT_ns.txt')

    # Generating random seed using secrets library
    seed = (prng.secrets.randbits(256)).to_bytes(32, byteorder='big')
    
    # Generating a pseudorandom number
    drbg = prng.DRBG(seed)
    random_bits = drbg.generate(len(bitstring))
    drbg_bits = ''.join(format(byte, '08b') for byte in random_bits)

    print(f'Entropy bitsring: {bitstring}')
    print(f'DRBG bitsring: {drbg_bits}')



if __name__ == "__main__":
    main()
