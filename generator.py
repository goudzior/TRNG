import os
import time
import threading
import hmac_drbg as prng
import round_trip_time as rtt

def read_random_url(file_path):
    # Reads a random URL from the specified file.
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return prng.secrets.choice(lines).strip()

def check_file_size_in_bits(file_path):
    # Returns the size of a given file in bits.
    with open(file_path, 'rb') as file:
        file.seek(0, os.SEEK_END)
        return file.tell() * 8

def extract_entropy(folder):
    # Collects entropy from binary files within a folder.
    entropy_bits = b''
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                entropy_bits += file.read()
    return entropy_bits

def combine_entropy_bits(entropy_list):
    # Combines multiple entropy byte arrays into one.
    return b''.join(entropy_list)

def trim_bits(value, num_bits):
    # Masks the value to retain only the most significant 'num_bits' bits.
    return value & ((1 << num_bits) - 1)

def clear_folder(folder):
    # Clears all files from the specified folder, creating it if it doesn't exist.
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

def create_rtt_threads(num_urls, url_data, rtt_folder, num_measurements):
    # Creates and starts threads for RTT measurements.
    threads = []
    for i in range(num_urls):
        url = 'https://' + read_random_url(url_data)
        rtt_file = os.path.join(rtt_folder, f'{i + 1}.txt')
        thread = threading.Thread(target=rtt.measure_rtt, args=(url, rtt_file, num_measurements))
        threads.append(thread)
        thread.start()
    return threads

def generate_random_number(num_urls, num_measurements, random_bytes, bit_length, rtt_folder, url_data):
    # Generates a random number.
    clear_folder(rtt_folder)
    threads = create_rtt_threads(num_urls, url_data, rtt_folder, num_measurements)
    for thread in threads:
        thread.join()

    entropy_bits = extract_entropy(rtt_folder)
    combined_entropy_bits = combine_entropy_bits([entropy_bits])
    seed = prng.secrets.randbits(256).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)
    prng_value = drbg.generate(random_bytes)

    prng_value = trim_bits(int.from_bytes(prng_value, 'big'), bit_length)
    combined_entropy_bits = trim_bits(int.from_bytes(combined_entropy_bits, 'big'), bit_length)
    random_number = prng_value ^ combined_entropy_bits

    return random_number

def main():
    num_iterations = 5
    num_urls = 2
    num_measurements = 2
    random_bytes = 2
    bit_length = 5
    rtt_folder = 'RTTS'
    url_data = 'top_websites100.txt'
 
    random_numbers = []

    start_time = time.time()
    for i in range(num_iterations):
        random_number = generate_random_number(num_urls, num_measurements, random_bytes, bit_length, rtt_folder, url_data)
        random_numbers.append(random_number)
    elapsed_time = time.time() - start_time

    print("Generated random numbers:")
    for i, number in enumerate(random_numbers, start=1):
        print(f"Iteration {i}: {number}")

    print(f"Total elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
