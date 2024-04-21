import hmac_drbg as prng
import round_trip_time as rtt


def main():
    url = 'https://' + input("Enter the URL to send HTTP GET request: ")
    num_measurements = 10
    filename = 'RTT_ns.txt'

    print("Measuring round trip times...")
    measurements = []
    for _ in range(num_measurements):
        round_trip_time = rtt.measure_round_trip_time(url)
        print(f"Round trip time: {round_trip_time} nanoseconds")
        measurements.append(round_trip_time)

    # Save round trip times to file
    rtt.save_to_file(measurements, filename)
    print(f"Round trip times saved to {filename}")

    # Generating random seed using secrets library
    seed = (prng.secrets.randbits(256)).to_bytes(32, byteorder='big')
    drbg = prng.DRBG(seed)


if __name__ == "__main__":
    main()
