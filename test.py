import math
import numpy as np

def shannons_entropy(data, max_value):
    total_count = len(data)
    freq_dict = {}
    for item in data:
        if item in freq_dict:
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1
    
    entropy = 0.0
    for count in freq_dict.values():
        probability = count / total_count
        entropy -= probability * math.log2(probability)
    
    max_bits = math.ceil(math.log2(max_value + 1))  # Calculate the number of bits needed to represent the largest value
    return entropy, max_bits

def read_file(filename):
    with open(filename, 'r') as file:
        data = [int(line.strip()) for line in file]
    return data

def main():
    filename = 'rtt_meas.txt'  # Change this to the filename of your larger numbers file
    data = read_file(filename)
    median_value = np.median(data)
    max_value = max(data)  # Find the largest number in the file
    entropy, max_bits = shannons_entropy(data, max_value)
    print("Shannon's entropy:", entropy)
    print("Maximum bits required to represent the largest value:", max_bits)
    print("Median:", median_value)

if __name__ == "__main__":
    main()
    