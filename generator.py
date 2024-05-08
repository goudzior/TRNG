import hmac_drbg as prng
import round_trip_time as rtt
import os
import time
import threading

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

def measure_rtt(url, rtt_file, num_measurements):
    for _ in range(num_measurements):
        round_trip_time = rtt.measure_round_trip_time(url)
        print(f"Round trip time for {url}: {round_trip_time} nanoseconds")
        with open(rtt_file, 'a') as file:
            file.write(str(round_trip_time) + '\n')
    print(f"Round trip times for {url} saved to {rtt_file}")

def main():
    start_time = time.time()

    MAX_THREADS = 16 
    random_bytes = 2

    num_measurements = 2 
    num_urls = 20

    rtt_folder= 'RTTS'
    url_data = 'top_websites100.txt'

    # Clear folder before measurments
    for filename in os.listdir(rtt_folder):
        file_path = os.path.join(rtt_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Error: {e}")

   # Create threads for measuring round-trip times
    threads = []
    for i in range(num_urls):
        url = 'https://' + read_random_url(url_data)
        rtt_file = os.path.join(rtt_folder, f'{i + 1}.txt')
        thread = threading.Thread(target=measure_rtt, args=(url, rtt_file, num_measurements))
        threads.append(thread)
        thread.start()

        # If the number of active threads reaches the maximum, wait for them to finish before starting new ones
        if len(threads) >= MAX_THREADS:
            for t in threads:
                t.join()
            threads = []  # Clear the threads list

    # Wait for any remaining threads to complete
    for thread in threads:
        thread.join()

    # Display the bitlength of rtt file
    # print(f"Bit length of rtt_ns.txt: {check_bitlength(rtt_data)} bits")
    # TODO => add health tests

    #bitstring = extract_entropy('RTT_ns.txt')
    
    # Generating a pseudorandom number
    seed = (prng.secrets.randbits(256)).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)
    prng_value = drbg.generate(random_bytes)

    # extracting entropy
    # entropy = extract_entropy('RTT_ns.txt')

    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
