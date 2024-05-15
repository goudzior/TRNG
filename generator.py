import os
import time
import concurrent.futures
import threading
import hmac_drbg as prng
import matplotlib.pyplot as plt
import numpy as np
import requests
from time import perf_counter_ns

# Global list to store all RTT measurements
all_rtt_measurements = []

def measure_rtt(url, rtt_file, num_measurements):
    local_measurements = []
    try:
        for _ in range(num_measurements):
            start_time = perf_counter_ns()
            response = requests.get(url)
            end_time = perf_counter_ns()
            round_trip_time = end_time - start_time
            local_measurements.append(round_trip_time)
        
        # Write the latest measurement to the file
        with open(rtt_file, 'w') as file:
            file.write(str(local_measurements[-1]) + '\n')

        # Append all measurements to the global list
        all_rtt_measurements.extend(local_measurements)

    except Exception as e:
        print(f"An error occurred: {e}")

def read_random_url(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return prng.secrets.choice(lines).strip()

def extract_entropy(folder):
    entropy_bits = b''
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                entropy_bits += file.read()
    return entropy_bits

def clear_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

def create_rtt_threads(num_urls, url_data, rtt_folder, num_measurements):
    threads = []
    for i in range(num_urls):
        url = 'https://' + read_random_url(url_data)
        rtt_file = os.path.join(rtt_folder, f'{i + 1}.txt')
        thread = threading.Thread(target=measure_rtt, args=(url, rtt_file, num_measurements))
        threads.append(thread)
        thread.start()
    return threads

def generate_random_number(num_urls, num_measurements, random_bytes, bit_length, rtt_folder, url_data):
    clear_folder(rtt_folder)
    threads = create_rtt_threads(num_urls, url_data, rtt_folder, num_measurements)
    for thread in threads:
        thread.join()

    entropy_bits = extract_entropy(rtt_folder)
    seed = prng.secrets.randbits(256).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)
    prng_value = drbg.generate(random_bytes)

    prng_value = int.from_bytes(prng_value, 'big') & ((1 << bit_length) - 1)
    entropy_bits = int.from_bytes(entropy_bits, 'big') & ((1 << bit_length) - 1)

    random_number = prng_value ^ entropy_bits
    return random_number

def main():
    start_time = time.perf_counter()
    num_iterations = 100500
    num_urls = 1
    num_measurements = 1
    random_bytes = 1 
    bit_length = 8
    rtt_folder = 'RTTS'
    url_data = 'top_websites2.txt'

    random_numbers = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_random_number, num_urls, num_measurements, random_bytes, bit_length, rtt_folder, url_data) for _ in range(num_iterations)]
        for future in concurrent.futures.as_completed(futures):
            try:
                random_numbers.append(future.result())
            except Exception as e:
                print(f"An error occurred: {e}")

    # Save random numbers to a text file
    with open('random_numbers.txt', 'w') as file:
        for number in random_numbers:
            file.write(f'{number}\n')

    num_bins = int(np.ceil(1 + np.log2(100000)))
    plt.figure(figsize=(10, 6))
    plt.hist(all_rtt_measurements, bins=317, color='blue', alpha=0.7, density=True)
    plt.title('Histogram of RTTs')
    plt.xlabel('RTT[ns]')
    plt.ylabel('Probability')
    plt.savefig('rtt_histogram.png')

    plt.figure(figsize=(10, 6))
    plt.hist(random_numbers, bins=256, color='green', alpha=0.7, density=True)
    plt.title('Histogram of random numbers')
    plt.xlabel('Value')
    plt.ylabel('Probability')
    plt.savefig('random.png')

    end_time = time.perf_counter()  # End the timer
    execution_time = end_time - start_time  # Calculate the total execution time

    # Write the contents of all RTT measurements to a file named "OH GOD"
    with open('rtt_meas.txt', 'w') as file:
        for rtt in all_rtt_measurements:
            file.write(f'{rtt}\n')
    
    print(f"Total execution time: {execution_time} seconds")

if __name__ == "__main__":
    main()

