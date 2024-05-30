import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(file_path):
    # Read data from file
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file if line.strip() != 'nan']  # Convert nanoseconds to seconds and filter out NaN values

    # Specify bin edges using an array
    bins = np.linspace(min(data), max(data), num=50)  # Adjust the number of bins as needed

    # Plot histogram
    plt.hist(data, bins=317, color='blue', alpha=0.7)
    plt.title('RTT measurments')
    plt.xlabel('RTT [ns]')
    plt.ylabel('Frequency')

    # Customize x-axis tick formatter to show scientific notation with exponent of 9
    plt.savefig('lol4')

# Example usage:
file_path = 'rtt_meas.txt'  # Replace 'data.txt' with the path to your file
plot_histogram(file_path)
