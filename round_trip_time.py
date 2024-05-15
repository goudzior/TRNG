import requests
from time import perf_counter_ns

def measure_rtt(url, rtt_file, num_measurements):
    try:
        with open(rtt_file, 'a') as file:
            for _ in range(num_measurements):
                start_time = perf_counter_ns()
                response = requests.get(url)
                end_time = perf_counter_ns()
                round_trip_time = end_time - start_time
                file.write(str(round_trip_time) + '\n')
    except Exception as e:
        print(f"An error occurred: {e}")

