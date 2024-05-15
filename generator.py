import os
import time
import concurrent.futures
import threading
import hmac_drbg as prng
import round_trip_time as rtt
import matplotlib.pyplot as plt
import numpy as np

def read_random_url(file_path):
    # Reads a random URL from the specified file.
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return prng.secrets.choice(lines).strip()

def extract_entropy(folder):
    # Collects entropy from binary files within a folder.
    entropy_bits = b''
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                entropy_bits += file.read().strip()
    return entropy_bits

def combine_entropy_bits(entropy_list):
    # Combines multiple entropy byte arrays into one.
    return b''.join(entropy_list).strip()

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
    seed = prng.secrets.randbits(256).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)
    prng_value = drbg.generate(random_bytes)

    prng_value = trim_bits(int.from_bytes(prng_value, 'big'), bit_length)
    entropy_bits = int.from_bytes(entropy_bits, 'big')

    random_number = prng_value ^ entropy_bits
    random_number = trim_bits(random_number, bit_length)

    return random_number

def calculate_entropy(random_numbers):
    # Calculate the entropy of the random numbers.
    probabilities, _ = np.histogram(random_numbers, bins=255, density=True)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))  # Add a small value to avoid log(0)
    return entropy

def main():
    num_iterations = 1000
    num_urls = 1
    num_measurements = 1
    random_bytes = 1
    bit_length = 8
    rtt_folder = 'RTTS'
    url_data = 'top_websites2.txt'

    random_numbers = []

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_random_number, num_urls, num_measurements, random_bytes, bit_length, rtt_folder, url_data) for _ in range(num_iterations)]
        for future in concurrent.futures.as_completed(futures):
            try:
                random_numbers.append(future.result())
            except Exception as e:
                print(f"An error occurred: {e}")

    elapsed_time = time.time() - start_time

    print(f"Total elapsed time: {elapsed_time:.2f} seconds")

    # Zapis wyników do pliku
    with open('random_numbers.txt', 'w') as file:
        for number in random_numbers:
            file.write(f'{number}\n')

    plt.figure(figsize=(8, 6))
    plt.hist(random_numbers, bins=256, color='blue', density=True)
    plt.title('Histogram of Randomly Generated Numbers')
    plt.xlabel('Value')
    plt.ylabel('Probability')
    plt.savefig("test")

    entropy = calculate_entropy(random_numbers)
    print(f"Entropy of random numbers: {entropy:.6f} bits per symbol")

if __name__ == "__main__":
    main()
