import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import argparse
import re

def plot_graph(files, output_file=None):
    fig, ax = plt.subplots(figsize=(7, 4))  # Set the figure size

    for file in files:
        data = pd.read_csv(file)

        # Convert the 'time' column to datetime
        data['time'] = pd.to_datetime(data['time'], unit='s')

        # Aggregate the data by minute and compute the average TPM
        data.set_index('time', inplace=True)
        data = data.resample('min').mean().reset_index()

        vUsers = re.search(r'\d+', file).group()

        ax.plot(data['time'], data['TPM'], label=vUsers + " vusers")

    # Set the title and labels
    ax.set_title('TPM during execution')
    ax.set_xlabel('Time in minutes')
    ax.set_ylabel('TPM')

    # Set xticks every minute
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))   # To get a tick every minute
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%M'))       # Tick format

    # Add a legend and place it below the plot with horizontal layout
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=len(files), fancybox=True, shadow=True)

    # Adjust the plot to make room for the legend
    plt.tight_layout()

    # Save the plot to a PDF file if output_file is specified
    if output_file:
        plt.savefig(output_file, format='pdf')
    else:
        # Show the plot if output_file is not specified
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot graph from CSV files.')
    parser.add_argument('files', nargs='+', help='The CSV files to plot')
    parser.add_argument('-export', metavar='output_file', help='Export the graph to a PDF file')
    args = parser.parse_args()

    plot_graph(args.files, args.export)

if __name__ == "__main__":
    main()
