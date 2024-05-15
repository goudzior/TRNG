import aiohttp
import asyncio
from time import perf_counter_ns

async def measure_round_trip_time(session, url):
    try:
        start_time = perf_counter_ns()
        async with session.get(url) as response:
            end_time = perf_counter_ns()
            round_trip_time = end_time - start_time
            return round_trip_time
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

async def measure_rtt(url, rtt_file, num_measurements):
    async with aiohttp.ClientSession() as session:
        for _ in range(num_measurements):
            round_trip_time = await measure_round_trip_time(session, url)
            if round_trip_time:
                #print(f"Round trip time for {url}: {round_trip_time} nanoseconds")
                with open(rtt_file, 'a') as file:
                    file.write(str(round_trip_time) + '\n')
            else:
                #print(f"Skipping URL {url} due to error")
                break  # Skip the URL and exit the loop

