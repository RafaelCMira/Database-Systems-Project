import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import argparse

def plot_graph(file):
    # Load the data from the CSV file
    data = pd.read_csv(file)

    # Convert the 'Timestamp' column to datetime
    data['time'] = pd.to_datetime(data['time'], unit='s')

    fig, ax = plt.subplots(figsize=(6,4))  # Set the figure size
    ax.plot(data['time'], data['TPM'])

    # Set the title and labels
    ax.set_title('TPM during execution')
    ax.set_xlabel('Time in minutes')
    ax.set_ylabel('TPM')

    # Set xticks every minute
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))   #to get a tick every minute
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))     #optional formatting

    # Show the plot
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot graph from CSV file.')
    parser.add_argument('file', help='The CSV file to plot')
    args = parser.parse_args()

    plot_graph(args.file)

if __name__ == "__main__":
    main()