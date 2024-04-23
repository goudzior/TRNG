import hmac_drbg as prng
import round_trip_time as rtt
import numpy as np
import csv


def main():
    num_measurements = 5
    num_urls = 5
    rtt_data = 'RTT_ns.txt'
    url_data = 'top_websites.txt'

    def read_random_url(file):
        with open(file, 'r') as file:
            # Read all lines from the text file
            lines = file.readlines()
            # Choose a random line (URL) from the list
            random_url = prng.secrets.choice(lines).strip()  # Strip to remove newline characters
        return random_url

    with open(rtt_data, 'w') as file:  # Open the file in write mode to clear its contents
        pass

    with open(rtt_data, 'a') as file:
        for i in range(num_urls):
            url = 'https://' + read_random_url(url_data)
            print(f"Measuring for: {url}")
            for _ in range(num_measurements):
                round_trip_time = rtt.measure_round_trip_time(url)
                print(f"Round trip time: {round_trip_time} nanoseconds")
                file.write(str(round_trip_time) + '\n')

    print(f"Round trip times saved to {rtt_data}")

    # check bitlength of rtt file
    with open('rtt_ns.txt', 'rb') as file:
        file.seek(0, 2)  # Move the file pointer to the end of the file
        bit_length = file.tell() * 8  # Get the byte length and convert it to bits
        print(f"Bit length of rtt_ns.txt: {bit_length} bits")

    # Generating random seed using secrets library
    seed = (prng.secrets.randbits(256)).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)


if __name__ == "__main__":
    main()
