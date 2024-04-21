import requests
import time

def measure_round_trip_time(url):
    start_time = time.time_ns()
    response = requests.get(url)
    end_time = time.time_ns()
    round_trip_time = end_time - start_time
    return round_trip_time

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(str(data) + '\n')

def main():
    url = input("Enter the URL to send HTTP GET request: ")
    num_measurements = 10
    filename = 'RTT_ns.txt'

    print("Measuring round trip times...")
    for _ in range(num_measurements):
        round_trip_time = measure_round_trip_time(url)
        print(f"Round trip time: {round_trip_time} nanoseconds")
        save_to_file(round_trip_time, filename)

    print(f"Round trip times saved to {filename}")

if __name__ == "__main__":
    main()
