import hmac_drbg as prng
import round_trip_time as rtt
import os
import time
import threading

# Reads x random urls from a file
def read_random_url(file):
    with open(file, 'r') as file:
        # Read all lines from the text file
        lines = file.readlines()
        # Choose a random line (URL) from the list
        random_url = prng.secrets.choice(lines).strip()  # Strip to remove newline characters
    return random_url

# Function to check bitlength of a given file
def check_bitlength(file):
    with open(file, 'rb') as file:
        file.seek(0, 2)  # Move the file pointer to the end of the file
        bit_length = file.tell() * 8  # Get the byte length and convert it to bits
    return bit_length

#------------------BIT OPERATIONS--------------------------
#Extracts entropy by reading a file as binary 
def extract_entropy(folder):
    entropy_bits = b''
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                bit_length = check_bitlength(file_path)
                with open(file_path, 'rb') as file:
                    # Read the file content as bytes
                    file_content = file.read()
                    # Append the bytes to the entropy bits
                    entropy_bits += file_content
        except Exception as e:
            print(f"Error extracting entropy from file {filename}: {e}")
    return entropy_bits

def combine_entropy_bits(entropy_list):
    combined_bits = b''
    for entropy_bits in entropy_list:
        entropy_bits = entropy_bits
        combined_bits += entropy_bits
    return combined_bits

def trim_bits(value, num_bits):
    # Masking to keep only the most significant bits
    mask = (1 << num_bits) - 1
    trimmed_value = value & mask
    return trimmed_value

def main():
    start_time = time.time()
    number_bitlength = 10
    random_bytes = 2

    num_measurements = 2 
    num_urls = 2

    rtt_folder= 'RTTS'
    url_data = 'top_websites100.txt'

    # Clear folder before measurements
    try:
        # Check if folder exists, if not, create it
        if not os.path.exists(rtt_folder):
            os.makedirs(rtt_folder)
        else:
            # If folder exists, delete its contents
            for filename in os.listdir(rtt_folder):
                file_path = os.path.join(rtt_folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting file: {e}")
    except Exception as e:
        print(f"Error: {e}")


   # Create threads for measuring round-trip times
    threads = []
    for i in range(num_urls):
        url = 'https://' + read_random_url(url_data)
        rtt_file = os.path.join(rtt_folder, f'{i + 1}.txt')
        thread = threading.Thread(target=rtt.measure_rtt, args=(url, rtt_file, num_measurements))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # TODO => add health tests

    
    # Generating a pseudorandom number
    seed = (prng.secrets.randbits(256)).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)
    prng_value = drbg.generate(random_bytes)


    # Extracting entropy from all measurments
    entropy_bits = extract_entropy(rtt_folder)
    combined_entropy_bits = combine_entropy_bits([entropy_bits])

    # Trim both PRNG value and combined entropy bits
    trimmed_prng_value = trim_bits(int.from_bytes(prng_value, "big"), number_bitlength)
    trimmed_combined_entropy_bits = trim_bits(int.from_bytes(combined_entropy_bits, "big"), number_bitlength)

    print(trimmed_prng_value)
    print(trimmed_combined_entropy_bits)

    random_number = trimmed_prng_value ^ trimmed_combined_entropy_bits

    print(f"Trimmed prng_value: {random_number}")

    #Code run-time
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    

if __name__ == "__main__":
    main()
