import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import argparse
import re

def plot_graph(files):
    fig, ax = plt.subplots(figsize=(7,4))  # Set the figure size

    for file in files:
        data = pd.read_csv(file)

        # Convert the 'Timestamp' column to datetime
        data['time'] = pd.to_datetime(data['time'], unit='s')

        number = re.search(r'\d+', file).group()

        ax.plot(data['time'], data['TPM'], label= number + " vusers")

    # Set the title and labels
    ax.set_title('TPM during execution')
    ax.set_xlabel('Time in minutes')
    ax.set_ylabel('TPM')

    # Set xticks every minute
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))   # To get a tick every minute
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))     # Tick format

    # Add a legend
    ax.legend()

    # Show the plot
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot graph from CSV files.')
    parser.add_argument('files', nargs='+', help='The CSV files to plot')
    args = parser.parse_args()

    plot_graph(args.files)

if __name__ == "__main__":
    main()