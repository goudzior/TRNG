import os
import time
import asyncio
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
                entropy_bits += file.read()
    return entropy_bits

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

async def create_rtt_threads(num_urls, url_data, rtt_folder, num_measurements):
    # Creates and starts threads for RTT measurements.
    tasks = []
    for i in range(num_urls):
        url = 'https://' + read_random_url(url_data)
        rtt_file = os.path.join(rtt_folder, f'{i + 1}.txt')
        task = asyncio.create_task(rtt.measure_rtt(url, rtt_file, num_measurements))
        tasks.append(task)
    await asyncio.gather(*tasks)

async def generate_random_number(num_urls, num_measurements, random_bytes, bit_length, rtt_folder, url_data):
    # Generates a random number.
    await create_rtt_threads(num_urls, url_data, rtt_folder, num_measurements)

    entropy_bits = extract_entropy(rtt_folder)
    seed = prng.secrets.randbits(256).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)
    prng_value = drbg.generate(random_bytes)

    prng_value = trim_bits(int.from_bytes(prng_value, 'big'), bit_length)
    entropy_bits = trim_bits(int.from_bytes(entropy_bits, 'big'), bit_length)
    #print (f"Prng: {prng_value} Entropy: {entropy_bits}  ")
    random_number = prng_value ^ entropy_bits

    return random_number

async def main():
    num_iterations = 10000  # Number of random numbers to generate
    num_urls = 1
    num_measurements = 2
    random_bytes = 1
    bit_length = 8
    rtt_folder = 'RTTS'
    url_data = 'top_websites2.txt'
    output_file = 'random_numbers.png'
 
    random_numbers = []

    start_time = time.time()
    for _ in range(num_iterations):
        random_number = await generate_random_number(num_urls, num_measurements, random_bytes, bit_length, rtt_folder, url_data)
        random_numbers.append(random_number)
    elapsed_time = time.time() - start_time

    print("Generated random numbers:")
    for i, number in enumerate(random_numbers, start=1):
        print(f"Iteration {i}: {number}")

    print(f"Total elapsed time: {elapsed_time:.2f} seconds")

    # Write results to a file
    with open('random_numbers.txt', 'w') as file:
        for number in random_numbers:
            file.write(f'{number}\n')

    # Calculate and print entropy
    #entropy = await calculate_entropy(random_numbers)
    #print(f"Entropy of random numbers: {entropy:.6f} bits per symbol")

    # Plot histogram
    plt.hist(random_numbers, bins=255, alpha=0.7, color='blue', density=True)  # Density set to True for probability
    plt.title('Histogram of random numbers')
    plt.xlabel('Value)')
    plt.ylabel('Probability')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')  # Save the plot as PNG file
    plt.show()

if __name__ == "__main__":
    asyncio.run(main())

